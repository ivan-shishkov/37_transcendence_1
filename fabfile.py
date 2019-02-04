import os

from fabric.api import env, run, cd, task, hide, settings
from fabtools import require, files, python, service, systemd

from fabric_set_env import set_env

env.REMOTE_HOST = os.environ['REMOTE_HOST']
env.hosts = [env.REMOTE_HOST]


def install_ubuntu_packages():
    require.deb.packages(
        pkg_list=[
            'git', 'python3-pip', 'nginx', 'postgresql', 'postgresql-contrib',
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
        require.git.working_copy(
            'https://github.com/ivan-shishkov/37_transcendence_1.git',
        )


def create_project_database():
    with hide('running'):
        require.postgres.user(
            name=env.PROJECT_DATABASE_USER,
            password=env.PROJECT_DATABASE_PASSWORD,
        )
    require.postgres.database(
        name=env.PROJECT_DATABASE_NAME,
        owner=env.PROJECT_DATABASE_USER,
        locale='en_US.utf8',
    )


def upload_project_env_variables(config_filename='.env'):
    require.files.template_file(
        path=os.path.join(env.PROJECT_DIR, config_filename),
        template_source=os.path.join('config_templates', config_filename),
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
    with python.virtualenv(env.PROJECT_VIRTUALENV_DIR), cd(env.PROJECT_DIR):
        python.install_requirements(filename='requirements.txt')


def run_project_management_commands():
    with python.virtualenv(env.PROJECT_VIRTUALENV_DIR), cd(env.PROJECT_DIR):
        run('python manage.py migrate')
        run('python manage.py collectstatic --no-input')
        create_django_admin_superuser()


def create_django_admin_superuser():
    prompts = {
        'Password: ': env.DJANGO_SUPERUSER_PASSWORD,
        'Password (again): ': env.DJANGO_SUPERUSER_PASSWORD,
    }
    with settings(hide('stdout'), prompts=prompts, warn_only=True):
        run(
            'python manage.py createsuperuser '
            '--username={username} --email={email}'.format(
                username=env.DJANGO_SUPERUSER_USERNAME,
                email=env.DJANGO_SUPERUSER_EMAIL,
            ),
        )


def create_project_configs_directory():
    require.files.directory(path=env.PROJECT_CONFIGS_DIR)


def upload_project_uwsgi_config():
    require.files.template_file(
        path=env.UWSGI_CONFIG_FILEPATH,
        template_source=os.path.join(
            'config_templates', env.UWSGI_CONFIG_FILENAME),
        context={
            'socket_filepath': env.SOCKET_FILEPATH,
            'project_dir': env.PROJECT_DIR,
            'project_virtualenv_dir': env.PROJECT_VIRTUALENV_DIR,
        },
    )


def upload_uwsgi_service_config(config_filename='uwsgi.service'):
    require.files.template_file(
        path=os.path.join('/etc/systemd/system', config_filename),
        template_source=os.path.join('config_templates', config_filename),
        context={
            'project_uwsgi_config_filepath': env.UWSGI_CONFIG_FILEPATH,
        },
        use_sudo=True,
        mode=644,
    )


def update_uwsgi_service(service_name='uwsgi'):
    systemd.restart(service_name)
    systemd.enable(service_name)


def upload_project_nginx_config():
    require.files.template_file(
        path=env.NGINX_CONFIG_FILEPATH,
        template_source=os.path.join(
            'config_templates', env.NGINX_CONFIG_FILENAME),
        context={
            'socket_filepath': env.SOCKET_FILEPATH,
            'server_name': env.REMOTE_HOST,
            'project_static_dir': os.path.join(env.PROJECT_DIR, 'static'),
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
    service.reload('nginx')


@task
def bootstrap():
    set_env(env)

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

    upload_uwsgi_service_config()
    update_uwsgi_service()

    upload_project_nginx_config()
    update_nginx_configuration()
