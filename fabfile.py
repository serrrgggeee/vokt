from fabric.api import *

import deploy.fabric.setup as setup

from fabric.utils import _AttributeDict

import os

env.project = _AttributeDict({
    'name': 'serrrgggeee',
    'username': 'serrrgggeee',  # group assumed to be the same
    'src_repo': 'git@bitbucket.org:serrrgggeee/voktyabr.git',
    'reqs': 'requirements.txt',
    'src_dir': 'source_tmp',  # rel from home
    'src_web': 'voktyabr',  # rel from home
    'src_branch': 'master',
    'pip_cache': '.pip-cache',  # rel path from home
    'venv': 'vokt',
    'touch_file': '/tmp/voktyabr.txt',

    'persistent_dirs': [
        {'media': [
            'cache',
            'ckeditor',
        ]}
    ],
    
    'links': [
        ('media', 'media'),  # 1 - rel from home, 2 - rel from src_web
        ('media', 'voktyabr/media'),  # 1 - rel from home, 2 - rel from src_web
    ],
})

env.project.home = os.path.join('/home', env.project.username)
env.project.pip = os.path.join(env.project.home, env.project.venv,
                               'bin', 'pip')
env.project.python = os.path.join(env.project.home, env.project.venv,
                                  'bin', 'python')


def co_branch():
    local('git checkout {branch}'.format(branch=env.project.src_branch))


def push():
    local('git push origin {branch}'.format(branch=env.project.src_branch))


@task(name='local')
def loc():
    env.type = 'local'
    env.hosts = ['localhost']
    co_branch()
    push()


@task
def prod():
    env.type = 'prod'
    env.hosts = [
        'root@78.155.219.56'
    ]
    co_branch()
    push()


@task
def full_deploy():
    setup.full()


@task
def web():
    setup.web()


@task
def complete_deploy():
    setup.complete()


try:
    from fabfile_local import *
except ImportError:
    pass

try:
    from fabfile_local import modify
    modify(globals())
except ImportError:
    pass
