import os

from fabric.api import env, run, cd, sudo, task, hide
from fabtools import require, files, supervisor, python, user

env.REMOTE_HOST = os.environ['REMOTE_HOST']
env.hosts = [env.REMOTE_HOST]


def set_env():
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

    env.REPO_URL = 'https://github.com/ivan-shishkov/37_transcendence_1.git'

    env.USER_HOME_DIR = user.home_directory(env.user)

    env.PROJECT_DIR = os.path.join(env.USER_HOME_DIR, '37_transcendence_1')
    env.PROJECT_VIRTUALENV_DIR = os.path.join(env.PROJECT_DIR, 'venv')
    env.PROJECT_CONFIGS_DIR = os.path.join(env.PROJECT_DIR, 'deploy_configs')
    env.PROJECT_STATIC_DIR = os.path.join(env.PROJECT_DIR, 'static')

    env.SOCKET_FILEPATH = os.path.join(env.PROJECT_DIR, 'social_network.sock')

    env.CONFIG_TEMPLATES_DIR = 'config_templates'

    env.ENV_CONFIG_FILENAME = '.env'
    env.ENV_CONFIG_FILEPATH = os.path.join(
        env.PROJECT_DIR, env.ENV_CONFIG_FILENAME)
    env.ENV_TEMPLATE_SOURCE = os.path.join(
        env.CONFIG_TEMPLATES_DIR, env.ENV_CONFIG_FILENAME)

    env.NGINX_CONFIG_FILENAME = 'social_network_nginx.conf'
    env.NGINX_CONFIG_FILEPATH = os.path.join(
        env.PROJECT_CONFIGS_DIR, env.NGINX_CONFIG_FILENAME)
    env.NGINX_TEMPLATE_SOURCE = os.path.join(
        env.CONFIG_TEMPLATES_DIR, env.NGINX_CONFIG_FILENAME)

    env.UWSGI_CONFIG_FILENAME = 'social_network_uwsgi.ini'
    env.UWSGI_CONFIG_FILEPATH = os.path.join(
        env.PROJECT_CONFIGS_DIR, env.UWSGI_CONFIG_FILENAME)
    env.UWSGI_TEMPLATE_SOURCE = os.path.join(
        env.CONFIG_TEMPLATES_DIR, env.UWSGI_CONFIG_FILENAME)

    env.SUPERVISOR_CONFIG_FILENAME = 'social_network_supervisor.conf'
    env.SUPERVISOR_CONFIG_FILEPATH = os.path.join(
        env.PROJECT_CONFIGS_DIR, env.SUPERVISOR_CONFIG_FILENAME)
    env.SUPERVISOR_TEMPLATE_SOURCE = os.path.join(
        env.CONFIG_TEMPLATES_DIR, env.SUPERVISOR_CONFIG_FILENAME)


def install_ubuntu_packages():
    require.deb.packages(
        pkg_list=[
            'git', 'python3-pip', 'nginx', 'supervisor',
            'postgresql', 'postgresql-contrib',
        ],
        update=True,
    )


def install_uwsgi(destination_filepath='/usr/bin/uwsgi', package_name='uwsgi',
                  pip_command='pip3'):
    if not python.is_installed(package=package_name, pip_cmd=pip_command):
        python.install(packages=[package_name], pip_cmd=pip_command)

    if not files.is_file(destination_filepath):
        files.copy(
            source=os.path.join(env.USER_HOME_DIR, '.local/bin/uwsgi'),
            destination=destination_filepath,
            use_sudo=True,
        )


def download_project_source_code():
    with cd(env.USER_HOME_DIR):
        require.git.working_copy(remote_url=env.REPO_URL)


def create_project_database():
    require.postgres.user(
        name=env.PROJECT_DATABASE_USER,
        password=env.PROJECT_DATABASE_PASSWORD,
    )
    require.postgres.database(
        name=env.PROJECT_DATABASE_NAME,
        owner=env.PROJECT_DATABASE_USER,
        locale='en_US.utf8',
    )


def upload_project_env_variables():
    require.files.template_file(
        path=env.ENV_CONFIG_FILEPATH,
        template_source=env.ENV_TEMPLATE_SOURCE,
        context={
            'secret_key': env.DJANGO_SECRET_KEY,
            'db_user': env.PROJECT_DATABASE_USER,
            'db_password': env.PROJECT_DATABASE_PASSWORD,
            'db_host': 'localhost',
            'db_name': env.PROJECT_DATABASE_NAME,
            'remote_host': env.REMOTE_HOST,
            'sentry_dsn': env.SENTRY_DSN,
        },
    )


def create_project_virtualenv():
    require.python.virtualenv(
        directory=env.PROJECT_VIRTUALENV_DIR, venv_python='python3.5')


def install_project_requirements():
    with python.virtualenv(env.PROJECT_VIRTUALENV_DIR):
        with cd(env.PROJECT_DIR):
            python.install_requirements(filename='requirements.txt')


def run_project_management_commands():
    with python.virtualenv(env.PROJECT_VIRTUALENV_DIR):
        with cd(env.PROJECT_DIR):
            run('python manage.py migrate')
            run('python manage.py collectstatic --no-input')
            create_django_admin_superuser()


def create_django_admin_superuser():
    create_superuser_code_template = """
from django.contrib.auth import get_user_model
    
User = get_user_model()
    
if User.objects.filter(username='{username}').count() == 0:
    User.objects.create_superuser(username='{username}', 
        email='{email}', password='{password}').save()
"""
    create_superuser_command = 'python manage.py shell -c "{}"'.format(
        create_superuser_code_template.format(
            username=env.DJANGO_SUPERUSER_USERNAME,
            email=env.DJANGO_SUPERUSER_EMAIL,
            password=env.DJANGO_SUPERUSER_PASSWORD,
        ),
    )
    with hide('running'):
        run(create_superuser_command)


def create_project_configs_directory():
    require.files.directory(path=env.PROJECT_CONFIGS_DIR)


def upload_project_uwsgi_config():
    require.files.template_file(
        path=env.UWSGI_CONFIG_FILEPATH,
        template_source=env.UWSGI_TEMPLATE_SOURCE,
        context={
            'socket_filepath': env.SOCKET_FILEPATH,
            'project_dir': env.PROJECT_DIR,
            'project_virtualenv_dir': env.PROJECT_VIRTUALENV_DIR,
        },
    )


def upload_project_supervisor_config():
    require.files.template_file(
        path=env.SUPERVISOR_CONFIG_FILEPATH,
        template_source=env.SUPERVISOR_TEMPLATE_SOURCE,
        context={
            'user': env.user,
            'project_dir': env.PROJECT_DIR,
            'project_uwsgi_config_filepath': env.UWSGI_CONFIG_FILEPATH,
        },
    )


def update_supervisor_configuration(
        destination_filepath='/etc/supervisor/conf.d/social-network.conf'):
    if not files.is_link(destination_filepath):
        files.symlink(
            source=env.SUPERVISOR_CONFIG_FILEPATH,
            destination=destination_filepath,
            use_sudo=True,
        )
    supervisor.update_config()


def upload_project_nginx_config():
    require.files.template_file(
        path=env.NGINX_CONFIG_FILEPATH,
        template_source=env.NGINX_TEMPLATE_SOURCE,
        context={
            'socket_filepath': env.SOCKET_FILEPATH,
            'server_name': env.REMOTE_HOST,
            'project_static_dir': env.PROJECT_STATIC_DIR,
        },
    )


def update_nginx_configuration(config_path='/etc/nginx/sites-enabled/'):
    default_config_filepath = os.path.join(config_path, 'default')
    project_config_filepath = os.path.join(
        config_path, env.NGINX_CONFIG_FILENAME)

    if files.is_link(default_config_filepath):
        files.remove(path=default_config_filepath, use_sudo=True)

    if not files.is_link(project_config_filepath):
        files.symlink(
            source=env.NGINX_CONFIG_FILEPATH,
            destination=project_config_filepath,
            use_sudo=True,
        )
    sudo('service nginx reload')


@task
def bootstrap():
    set_env()

    install_ubuntu_packages()
    install_uwsgi()

    download_project_source_code()

    create_project_database()

    upload_project_env_variables()

    create_project_virtualenv()
    install_project_requirements()
    run_project_management_commands()

    create_project_configs_directory()

    upload_project_uwsgi_config()
    upload_project_supervisor_config()
    update_supervisor_configuration()
    upload_project_nginx_config()
    update_nginx_configuration()
