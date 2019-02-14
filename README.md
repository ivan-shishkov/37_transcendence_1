# Transcendence project

This project is a simplified version of a social network developed using the [Django](https://www.djangoproject.com/) web framework.
An online version of the latest version of the project is available [here](http://83.220.170.27/).

# Used Environment Variables

* **DJANGO_CONFIGURATION** - a configuration to run the project (can be either **Dev** (development) or **Prod** (production))
* **DJANGO_SECRET_KEY** - a [secret key](https://docs.djangoproject.com/en/2.1/ref/settings/#std:setting-SECRET_KEY)
* **DJANGO_DATABASE_URI** - a database URI (The database must be either **SQLite** or **PostgreSQL**)
* **DJANGO_ALLOWED_HOSTS** - a [list of strings](https://docs.djangoproject.com/en/2.1/ref/settings/#std:setting-ALLOWED_HOSTS) representing the host/domain names that this Django site can serve (**only for production**)
* **DJANGO_MEDIA_ROOT** - an [absolute filesystem path](https://docs.djangoproject.com/en/2.1/ref/settings/#media-root) to the directory that will hold user-uploaded files.
* **SENTRY_DSN** - a [Sentry DSN](https://docs.sentry.io/error-reporting/configuration/?platform=python#dsn) for [Sentry](https://docs.sentry.io/) error tracking system (**only for production**)

# Launch on localhost

For project launch need to install Python 3.5 and then install all dependencies:

```bash

$ pip install -r requirements.txt

```

and then set the necessary environment variables:

```bash

$ export DJANGO_CONFIGURATION='Dev'
$ export DJANGO_SECRET_KEY='your_secret_key'
$ export DJANGO_DATABASE_URI='your_database_uri'
$ export DJANGO_MEDIA_ROOT='/absolute/path/to/media/'

```

To create all the necessary tables in the database you need to run:

```bash

$ python manage.py migrate

```

To create the superuser of the admin interface you need to run:

```bash

$ python manage.py createsuperuser

```

To project launch you need to run:

```bash

$ python manage.py runserver

```

After that you can log in to admin interface on [http://localhost:8000/admin/](http://localhost:8000/admin/) and create new users of social network.

All created users will have personal pages available on **http://localhost:8000/users/<user_id>/** (e.g. http://localhost:8000/users/1/).

# Deploy on Production Server

To deploy the project, you must use the server with **Ubuntu 16.04 LTS** installed.
In addition, a user must be created on the server who has the right to execute the **sudo** command.

For project deploy need to install Python 3.5 and then install dependencies:

```bash

$ pip install -r requirements-deploy.txt

```
then create the file with deployment parameters (e.g. **deploy_params.txt**) and set the necessary parameters:

* **REMOTE_HOST** - a remote server (e.g. 123.123.123.123)
* **REMOTE_HOST_USERNAME** - a username on the remote server
* **REMOTE_HOST_PASSWORD** - a user password on the remote server
* **REMOTE_HOST_SSH_PORT** - a port number for SSH connection (e.g. 22)
* **PROJECT_DATABASE_USER** - a database username
* **PROJECT_DATABASE_PASSWORD** - a database user password
* **PROJECT_DATABASE_NAME** - a project database name
* **DJANGO_SECRET_KEY** - a Django secret key (see above)
* **DJANGO_SUPERUSER_USERNAME** - a superuser name for the Django admin interface
* **DJANGO_SUPERUSER_EMAIL** - a superuser e-mail for the Django admin interface
* **DJANGO_SUPERUSER_PASSWORD** - a superuser password for the Django admin interface
* **SENTRY_DSN** - a Sentry DSN (see above)

All parameters should be in form **export PARAMETER='your_parameter_value'**, e.g.:

```bash

export REMOTE_HOST='your_remote_host'
export REMOTE_HOST_USERNAME='your_remote_host_username'
export REMOTE_HOST_PASSWORD='your_remote_host_password'
export REMOTE_HOST_SSH_PORT='22'
export PROJECT_DATABASE_USER='your_project_database_user'
export PROJECT_DATABASE_PASSWORD='your_project_database_password'
export PROJECT_DATABASE_NAME='your_project_database_name'
export DJANGO_SECRET_KEY='your_django_secret_key'
export DJANGO_SUPERUSER_USERNAME='your_superuser_username'
export DJANGO_SUPERUSER_EMAIL='your_superuser_email'
export DJANGO_SUPERUSER_PASSWORD='your_superuser_password'
export SENTRY_DSN='your_sentry_dsn'

```

Then execute the deployment of project on the remote server:

```bash

$ source deploy_params.txt
$ fab bootstrap

```

After completion of the deployment process, the project will be available via a web browser.

If you only need to update the source code of the project, then you can use the light version of the deployment command:

```bash

$ fab deploy

```

# Project Goals

The code is written for educational purposes. Training course for web-developers - [DEVMAN.org](https://devman.org)
