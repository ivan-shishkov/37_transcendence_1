# Transcendence project

This project is a simplified version of a social network developed using the [Django](https://www.djangoproject.com/) web framework.

# Used Environment Variables

* **DJANGO_CONFIGURATION** - a configuration to run the project (maybe either **Dev** (development) or **Prod** (production))
* **DJANGO_SECRET_KEY** - a [secret key](https://docs.djangoproject.com/en/2.1/ref/settings/#std:setting-SECRET_KEY)
* **DJANGO_DATABASE_URI** - a database URI
* **DJANGO_ALLOWED_HOSTS** - a [list of strings](https://docs.djangoproject.com/en/2.1/ref/settings/#std:setting-ALLOWED_HOSTS) representing the host/domain names that this Django site can serve (**only for production**)
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

# Project Goals

The code is written for educational purposes. Training course for web-developers - [DEVMAN.org](https://devman.org)
