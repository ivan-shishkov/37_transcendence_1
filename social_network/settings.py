import os

from configurations import Configuration, values
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration


class BaseConfiguration(Configuration):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    SECRET_KEY = values.SecretValue()

    INSTALLED_APPS = [
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',

        'captcha',
        'easy_thumbnails',
        'bootstrap4',
        'django_registration',

        'users.apps.UsersConfig',
        'pages.apps.PagesConfig',
    ]

    MIDDLEWARE = [
        'django.middleware.security.SecurityMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    ]

    ROOT_URLCONF = 'social_network.urls'

    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [os.path.join(BASE_DIR, 'templates')],
            'APP_DIRS': True,
            'OPTIONS': {
                'context_processors': [
                    'django.template.context_processors.debug',
                    'django.template.context_processors.request',
                    'django.contrib.auth.context_processors.auth',
                    'django.contrib.messages.context_processors.messages',
                ],
            },
        },
    ]

    WSGI_APPLICATION = 'social_network.wsgi.application'

    DATABASES = values.DatabaseURLValue(
        values.Value(environ_name='DATABASE_URI', environ_required=True),
    )

    AUTH_PASSWORD_VALIDATORS = [
        {
            'NAME': 'django.contrib.auth.password_validation.'
                    'UserAttributeSimilarityValidator',
        },
        {
            'NAME': 'django.contrib.auth.password_validation.'
                    'MinimumLengthValidator',
        },
        {
            'NAME': 'django.contrib.auth.password_validation.'
                    'CommonPasswordValidator',
        },
        {
            'NAME': 'django.contrib.auth.password_validation.'
                    'NumericPasswordValidator',
        },
    ]

    LANGUAGE_CODE = 'en-us'

    TIME_ZONE = 'UTC'

    USE_I18N = True

    USE_L10N = True

    USE_TZ = True

    STATIC_URL = '/static/'

    STATIC_ROOT = os.path.join(BASE_DIR, 'static')

    MEDIA_URL = '/media/'

    MEDIA_ROOT = values.Value(environ_required=True)

    AUTH_USER_MODEL = 'users.CustomUser'

    LOGIN_REDIRECT_URL = 'pages:home'

    LOGOUT_REDIRECT_URL = 'pages:home'

    LOGIN_URL = 'users:login'

    BOOTSTRAP4 = {
        'success_css_class': '',
    }


class Dev(BaseConfiguration):
    DEBUG = True

    ALLOWED_HOSTS = []


class Prod(BaseConfiguration):
    DEBUG = False

    ALLOWED_HOSTS = values.ListValue(environ_required=True)

    SENTRY_DSN = values.Value(environ_prefix=None, environ_required=True)

    @classmethod
    def post_setup(cls):
        super(Prod, cls).post_setup()

        sentry_sdk.init(
            dsn=cls.SENTRY_DSN,
            integrations=[DjangoIntegration()],
        )
