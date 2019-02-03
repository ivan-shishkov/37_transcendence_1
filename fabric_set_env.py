import os

from fabtools import user


def set_env(env):
    env.colorize_errors = True

    env.user = os.environ['REMOTE_HOST_USERNAME']
    env.password = os.environ['REMOTE_HOST_PASSWORD']
    env.port = os.environ['REMOTE_HOST_SSH_PORT']

    env.PROJECT_DATABASE_USER = os.environ['PROJECT_DATABASE_USER']
    env.PROJECT_DATABASE_PASSWORD = os.environ['PROJECT_DATABASE_PASSWORD']
    env.PROJECT_DATABASE_NAME = os.environ['PROJECT_DATABASE_NAME']

    env.DJANGO_SECRET_KEY = os.environ['DJANGO_SECRET_KEY']
    env.DJANGO_SUPERUSER_USERNAME = os.environ['DJANGO_SUPERUSER_USERNAME']
    env.DJANGO_SUPERUSER_EMAIL = os.environ['DJANGO_SUPERUSER_EMAIL']
    env.DJANGO_SUPERUSER_PASSWORD = os.environ['DJANGO_SUPERUSER_PASSWORD']

    env.SENTRY_DSN = os.environ['SENTRY_DSN']

    env.USER_HOME_DIR = user.home_directory(env.user)

    env.PROJECT_DIR = os.path.join(env.USER_HOME_DIR, '37_transcendence_1')
    env.PROJECT_VIRTUALENV_DIR = os.path.join(env.PROJECT_DIR, 'venv')
    env.PROJECT_CONFIGS_DIR = os.path.join(env.PROJECT_DIR, 'deploy_configs')

    env.SOCKET_FILEPATH = os.path.join(env.PROJECT_DIR, 'social_network.sock')

    env.NGINX_CONFIG_FILENAME = 'social_network_nginx.conf'
    env.NGINX_CONFIG_FILEPATH = os.path.join(
        env.PROJECT_CONFIGS_DIR, env.NGINX_CONFIG_FILENAME)

    env.UWSGI_CONFIG_FILENAME = 'social_network_uwsgi.ini'
    env.UWSGI_CONFIG_FILEPATH = os.path.join(
        env.PROJECT_CONFIGS_DIR, env.UWSGI_CONFIG_FILENAME)
