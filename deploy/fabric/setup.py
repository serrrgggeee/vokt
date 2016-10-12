import os

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS_DIR = os.path.join(PROJECT_DIR)
import fabtools
from fabric.api import *
import rabbit as rabbit_require
import fabtools.require.files as rfiles
# from fabtools.require.redis import instance as redis_instance
from deploy.fabric.redis import instance as redis_instance

from fabric.contrib.files import exists, append
from fabric.context_managers import shell_env
def sudo_project(*args, **kwargs):
    kwargs.update({
        'user': env.project.username,
        'group': env.project.username
    })
    return sudo(*args, **kwargs)


def manage(cmd):
    # src path should be set by caller
    with cd(env.src_path):
        return sudo_project('%s %s %s' % (env.project.python, env.project.manage, cmd))


def update_code(src_path):
    with cd(src_path):

        sudo_project('git pull origin master')
        sudo_project('git checkout %s' % env.project.src_branch)


def require_packages(requirements_path):
    with open(requirements_path, 'r') as req_file:
        packages = req_file.readlines()
    clean = lambda s: s.strip('\n')
    packages = map(clean, packages)
    print "Following packages required:", packages
    fabtools.require.deb.packages(packages, update=True)


def project_user():
    username = env.project.username
    home = '/home/%s' % username

    if not fabtools.user.exists(username):
        fabtools.user.create(username, home=home, shell='/bin/bash')

    fabtools.require.directory(home, owner=username, group=username,
                               use_sudo=True)

    # sudo('chgrp %s /opt ' % username)
    # sudo('chmod 775 /opt')

    fabtools.require.directory('/var/log/%s' % username, owner=username,
                               group=username, use_sudo=True)

def supervisord():
    # Supervisord
    sudo('easy_install supervisor')
    pjt_dir = os.path.dirname(DOCS_DIR)
    init_script = os.path.join(pjt_dir, 'deploy', 'supervisord.sh')
    put(local_path=init_script, remote_path='/etc/init.d/supervisord', use_sudo=True, mode=0755)
    sudo('update-rc.d supervisord start 99 2 3 4 5 .')
    sudo('echo_supervisord_conf > /etc/supervisord.conf')
    import fabtools.require.files
    import fabric.contrib.files as fcon

    fabtools.require.directory('/etc/supervisor.d/', owner='root', group='root', use_sudo=True)
    fcon.append('/etc/supervisord.conf', '[include]', use_sudo=True)
    fcon.append('/etc/supervisord.conf', 'files = /etc/supervisor.d/*.conf', use_sudo=True)
    sudo('/etc/init.d/supervisord start')


def postgresql():
    sudo('wget --quiet -O - http://apt.postgresql.org/pub/repos/apt/ACCC4CF8.asc | apt-key add -')
    fabtools.require.deb.source('pgdg', 'http://apt.postgresql.org/pub/repos/apt/', 'precise-pgdg', 'main')
    fabtools.require.postgres.server(version='9.5')
    fabtools.require.postgres.user('serrrgggeee', 'Tktyf,firjdf1')
    fabtools.require.postgres.database('vokt', owner='serrrgggeee')


def mongodb():
    sudo('apt-key adv --keyserver keyserver.ubuntu.com --recv 7F0CEB10')
    fabtools.require.deb.source('mongodb', 'http://downloads-distro.mongodb.org/repo/ubuntu-upstart', 'dist', '10gen')
    fabtools.require.deb.package('mongodb-10gen', update=True)


def nginx():
    fabtools.require.deb.ppa('ppa:nginx/stable')
    fabtools.require.deb.package('nginx', update=True)
    copy_file(
        src=os.path.join(env.src_path, 'deploy/nginx.conf'),
        dst='/etc/nginx/sites-enabled/voktyabr.conf'
    )


def rabbit():
    with cd('/tmp'):
        if not fabtools.files.is_file('rabbitmq-signing-key-public.asc'):
            fabtools.files.run('wget http://www.rabbitmq.com/rabbitmq-signing-key-public.asc')
        fabtools.deb.add_apt_key('rabbitmq-signing-key-public.asc')
    fabtools.require.deb.package('rabbitmq-server', update=True)
    rabbit_require.user(env.celery.username, env.celery.password)
    rabbit_require.vhost(env.celery.vhost)
    rabbit_require.set_permissions(env.celery.vhost, env.celery.username)


def redis():
    conf = {
        'requirepass': '2aMeV3esS14Q3u24G25TiF0Vt'
    }

    redis_instance(name='celery', version='3.0.5', bind='127.0.0.1', port=6379, **conf)


def python():
    username = env.project.username
    home = '/home/%s' % username
    repo = env.project.src_repo
    path = '%s/%s' % (home, env.project.src_dir)

    # Clean old installation
    if fabtools.files.is_dir(path):
        sudo('rm -rf %s' % path)

    # Cloning:
    with cd(home):
        sudo_project('git clone -q {repo} {dest}'.format(repo=repo, dest=path))

    # Co needed branch
    with cd(path):
        sudo_project('git checkout %s' % env.project.src_branch)

    with cd(path):
        sudo_project('git pull')

    sudo('cp -f {src} {dst}'.format(src=path + '/deploy/locale.gen', dst='/etc/locale.gen'))

    # Creating venv
    venv = '%s/%s' % (home, env.project.venv)
    pip = '%s/bin/pip' % venv
    with cd(home):
        if not fabtools.files.is_dir(venv):
            sudo_project('virtualenv --python=python3.4 %s' % venv)
            sudo_project('%s install --upgrade pip' % pip)
            # Fucking PIL. HACK
            with settings(hide('running', 'stdout', 'stderr'), warn_only=True):
                sudo('ln -s /usr/lib/x86_64-linux-gnu/libjpeg.so /usr/lib')
                sudo('ln -s /usr/lib/x86_64-linux-gnu/libfreetype.so /usr/lib')
                sudo('ln -s /usr/lib/x86_64-linux-gnu/libz.so /usr/lib')
        reqs = '%s/%s' % (path, env.project.reqs)
        cache_dir = os.path.join(home, env.project.pip_cache)
        fabtools.require.directory(cache_dir, use_sudo=True, owner=env.project.username, group=env.project.username)
        sudo_project('{pip} install -r {reqs}  --no-binary :all'.format(pip=pip, reqs=reqs))
        pers_dirs = env.project.get('persistent_dirs', [])
        process_persistent_dirs(pers_dirs)


def make_links(src_path):
    for link_target, link_path in env.project.links:
        lt = os.path.join(env.project.home, link_target)
        fabtools.require.directory(lt, use_sudo=True, owner=env.project.username, group=env.project.username)
        lp = os.path.join(src_path, link_path)
        sudo_project('ln -s %s %s' % (lt, lp))


def process_persistent_dirs(conf_list):
    def _req_dir(path):
        rfiles.directory(path, use_sudo=True, owner=env.project.username, group=env.project.username)

    def _process(parent, lst):
        for item in lst:
            if isinstance(item, basestring):
                _req_dir(os.path.join(parent, item))
            elif isinstance(item, dict):
                for key, val in item.iteritems():
                    p = os.path.join(parent, key)
                    _req_dir(p)
                    _process(p, val)
            else:
                raise AssertionError(u'Unknown item: %s, class: %s' % (item, item.__class__))
    _process(env.project.home, conf_list)


def make_static(src_path):
    print('copydone')
    with cd(src_path):
        manage('collectstatic --noinput --ignore=cache --ignore=upload --ignore=multiuploader_images')


def copy_project(src_path):
    copied_src = os.path.join(env.project.home, 'web_new')
    with settings(hide('stdout'), warn_only=True):
        sudo('rm -rf %s' % copied_src)
    sudo_project('cp -R %s %s' % (src_path, copied_src))
    return copied_src


def migrate_db(src_path):
    with cd(src_path):
        manage('syncdb --noinput')
        manage('migrate')


def migrate_db2(src_path):
    with cd(src_path):
        with shell_env(PGHOST='localhost'):
            print('migration')
            manage('migrate')


def move_project(src_path):
    pjt = os.path.join(env.project.home, env.project.src_web)
    old = os.path.join(env.project.home, 'web_old')
    if fabtools.files.is_dir(pjt) and fabtools.files.is_dir(old):
        with settings(warn_only=True):
            sudo('rm -rf %s' % old)
    if fabtools.files.is_dir(pjt):
        with settings(warn_only=True):
            sudo('mv %s %s' % (pjt, old))
    print(src_path, 'pjt', pjt)
    sudo('mv %s %s' % (src_path, pjt))

    return pjt, old


def clean_project(old):
    with settings(hide('stdout'), warn_only=True):
        sudo('rm -rf %s' % old)


def restart_celery():
    config = os.path.join(
        env.project.home,
        env.project.src_web,
        'voktyabr.conf'
    )
    # Ensure that our config is included:
    sup_conf = '/etc/supervisor.d/%s.conf' % env.project.name
    sudo('rm -f %s' % sup_conf)
    sudo('ln -s {conf} {sup}'.format(sup=sup_conf, conf=config))

    fabtools.supervisor.update_config()

    if fabtools.supervisor.process_status('redis_celery') != 'RUNNING':
        fabtools.supervisor.start_process('redis_celery')

    fabtools.supervisor.restart_process('voktyabrbeat')

    with settings(warn_only=True):
        sudo('update-rc.d supervisord defaults')
        # sudo('update-rc.d rabbitmq-server defaults'.format(env.project.name))
        sudo('update-rc.d rabbitmq-server defaults')


def restart_web(full=False):
    if not full:
        touch_file = os.path.join(env.project.home, env.project.src_web, env.project.touch)
        sudo('touch %s' % touch_file)
        return
    # We are doing full deploy
    sudo('/etc/init.d/nginx reload')
    # Verify that nginx started
    if not fabtools.require.service.is_running('nginx'):
        fabtools.require.service.start('nginx')
    with settings(warn_only=True):
        sudo('update-rc.d nginx defaults')
        sudo('update-rc.d uwsgi.{0} defaults'.format(env.project.name))
    sudo('/etc/init.d/uwsgi.{0} force-reload'.format(env.project.name))


def make_persistent():
    pd = env.project.get('persistent_dirs', [])
    process_persistent_dirs(pd)


def copy_settings(src_path):
    sudo('cp -f {src} {dst}'.format(src=src_path+'/deploy/settings.py', dst=src_path+'/voktyabr/voktyabr/local_settings.py'))
    sudo('cp -f {src} {dst}'.format(src=src_path+'/deploy/server.vokt', dst='/etc/init.d/server.vokt'))
    sudo('chmod 755 /etc/init.d/server.vokt')

    if not exists('/etc/rc1.d/K20server.vokt'):
        sudo('update-rc.d server.vokt defaults')


def restart_service(name):
    if fabtools.service.is_running(name):
        fabtools.service.restart(name)
    else:
        fabtools.service.start(name)


def copy_file(src, dst):
    sudo('cp -f {src} {dst}'.format(src=src, dst=dst))


def tor():
    copy_file(
        src=os.path.join(env.src_path, 'deploy/torrc'),
        dst='/etc/tor/torrc'
    )

    restart_service('tor')


def pgbouncer():
    copy_file(
        src=os.path.join(env.src_path, 'deploy/pgbouncer/pgbouncer.ini'),
        dst='/etc/pgbouncer/pgbouncer.ini'
    )
    copy_file(
        src=os.path.join(env.src_path, 'deploy/pgbouncer/userlist.txt'),
        dst='/etc/pgbouncer/userlist.txt'
    )

    restart_service('pgbouncer')


def privoxy():
    copy_file(
        src=os.path.join(env.src_path, 'deploy/privoxy_config'),
        dst='/etc/privoxy/config'
    )

    restart_service('privoxy')


def phantomjs():
    sudo('curl -sL https://deb.nodesource.com/setup | bash -')
    fabtools.require.deb.package(['nodejs'], update=True)
    sudo('npm install -g phantomjs')


# def bash_edit():
#     filename =  '/root/.bashrc'
#     text = 'export PGHOST="localhost"'
#     append(filename, text, use_sudo=True, partial=False, escape=True, shell=False)

#####################

@task
def postgresqldb():
    postgresql()


@task
def mongo():
    mongodb()


@task
def supervisor():
    supervisord()


@task
def rabbitmq():
    rabbit()


@task
def full():
    src_path = os.path.join(env.project.home, env.project.src_dir)
    env.src_path = src_path

    require_packages(os.path.join(os.path.dirname(DOCS_DIR), 'apt_web.txt'))
    #
    project_user()
    #
    python()

    nginx()
    ## pgbouncer()
    postgresql()
    #redis()
    supervisord()
    ## mongodb()
    #rabbit()

    #tor()
    #privoxy()
    #phantomjs()

    src_path = env.src_path = copy_project(src_path)
    print('src_path', src_path)
    env.project.manage = os.path.join(src_path, 'voktyabr', 'manage.py')
    venv = os.path.join(env.project.home, env.project.venv)
    with fabtools.python.virtualenv(venv):
        fabtools.require.python.requirements(
            os.path.join(src_path, env.project.reqs),
            use_sudo=True,
            user=env.project.username
        )
    copy_settings(src_path)
    make_links(src_path)

    make_static(src_path)
    migrate_db2(src_path)

    pjt, old = move_project(src_path)

    clean_project(old)

    sudo('/etc/init.d/server.vokt restart')

    ##run('crontab /home/root/voktyabr/voktyabr/crontab')

    #3fabtools.require.files.directory('/home/root/voktyabr/tmp')
    ##sudo('chown root:root /home/root/voktyabr/tmp')

    #restart_celery()


@task
def web_celery():
    src_path = os.path.join(env.project.home, env.project.src_web)
    env.src_path = src_path
    env.project.manage = os.path.join(src_path, 'voktyabr', 'manage.py')

    update_code(src_path)

    copy_settings(src_path)
    make_persistent()
    make_static(src_path)

    sudo('/etc/init.d/server.vokt restart')

    restart_celery()


@task
def web():
    src_path = os.path.join(env.project.home, env.project.src_web)
    env.src_path = src_path
    env.project.manage = os.path.join(src_path, 'voktyabr', 'manage.py')

    update_code(src_path)

    copy_settings(src_path)
    make_static(src_path)

    sudo('/etc/init.d/server.vokt restart')


@task
def complete():
    src_path = os.path.join(env.project.home, env.project.src_web)
    env.src_path = src_path
    env.project.manage = os.path.join(src_path, 'voktyabr', 'manage.py')

    update_code(src_path)

    copy_settings(src_path)
    make_persistent()
    make_static(src_path)
    migrate_db2(src_path)

    sudo('/etc/init.d/server.vokt restart')

    restart_celery()


@task
def celery():
    redis()
    supervisord()

#
# @task
# def bash_edit_task():
#     bash_edit()