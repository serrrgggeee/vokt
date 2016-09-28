from fabric.api import settings, sudo, hide


def vhost_exists(vhost_name):
    with settings(hide('running', 'stdout'), warn_only=True):
        return sudo('rabbitmqctl list_vhosts | grep -c {0}'.format(vhost_name)) >= '1'


def user_exists(username):
    with settings(hide('running', 'stdout'), warn_only=True):
        return sudo('rabbitmqctl list_users | grep -c {0}'.format(username)) >= '1'


def create_vhost(vhost_name):
    sudo('rabbitmqctl add_vhost {vhost}'.format(vhost=vhost_name))


def create_user(username, password):
    sudo('rabbitmqctl add_user {username} {password}'.format(username=username, password=password))


def set_permissions(vhost, user):
    sudo('rabbitmqctl set_permissions -p {vhost} {user} ".*" ".*" ".*"'.format(vhost=vhost, user=user))


def vhost(vhost_name):
    if not vhost_exists(vhost_name):
        create_vhost(vhost_name)


def user(username, password):
    if not user_exists(username):
        create_user(username, password)