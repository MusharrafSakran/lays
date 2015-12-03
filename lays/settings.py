"""
Django settings for lays project.

Generated by 'django-admin startproject' using Django 1.8.5.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
ENV = ''
try:
    with open('/etc/lays-env.txt') as f:
        ENV = f.read().strip()
except IOError, exp:
    ENV = 'LOCAL'
    pass

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
try:
    with open('/etc/lays-secret-key.txt') as f:
        SECRET_KEY = f.read().strip()
except IOError, exp:
    pass


# SECURITY WARNING: don't run with debug turned on in production!
if ENV == 'PRODUCTION':
    DEBUG = False
    ALLOWED_HOSTS = ['util.services', ]
    # CSRF_COOKIE_SECURE = True
    # SESSION_COOKIE_SECURE = True
    STATIC_ROOT = os.path.join(BASE_DIR, "static_files/")
    STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'
else:
    DEBUG = True
    ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'api',
    'rest_framework',
    'rest_framework_swagger',
    'public',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'lays.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
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

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),
    'DEFAULT_THROTTLE_CLASSES': (
        'rest_framework.throttling.AnonRateThrottle',
    ),
    'DEFAULT_THROTTLE_RATES': {
        'anon': '175/day',
    },
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.AcceptHeaderVersioning',
    'DEFAULT_VERSION': '1.0'
}

SWAGGER_SETTINGS = {
    # 'exclude_namespaces': [],
    'api_version': '1.0',
    'api_path': '/',
    # 'enabled_methods': [
    #     'get',
    #     'post',
    #     'put',
    #     'patch',
    #     'delete'
    # ],
    # 'api_key': '',
    # 'is_authenticated': False,
    # 'is_superuser': False,
    # 'permission_denied_handler': None,
    # 'resource_access_handler': None,
    # 'base_path':'helloreverb.com/docs',
    'info': {
        'contact': 'musharraf.altamimi@gmail.com',
        'description': 'This is a development util services API, '
                       'Services that are widely used by developers and they are hard to implement, '
                       'We implemented it once and make it able to use infinitely, '
                       'made with love by Developers to Developers.',
        # 'license': 'Apache 2.0',
        # 'licenseUrl': 'http://www.apache.org/licenses/LICENSE-2.0.html',
        'termsOfServiceUrl': '',
        'title': 'Util Services API',
    },
    'doc_expansion': 'list',
}

WSGI_APPLICATION = 'lays.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

if ENV == 'PRODUCTION':
    db_password = ''
    try:
        with open('/etc/lays-db-password.txt') as f:
            db_password = f.read().strip()
    except IOError, exp:
        pass
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'LAYS',
            'USER': 'lays',
            'PASSWORD': db_password,
            'HOST': 'localhost',  # Or an IP Address that your DB is hosted on
            'PORT': '3306',
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt': "%d/%b/%Y %H:%M:%S"
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'mysite.log',
            'formatter': 'verbose',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'propagate': True,
            'level': 'DEBUG',
        },
        'djangocon': {
            'handlers': ['console'],
            'propagate': True,
            'level': 'INFO',
        },
        'api': {
            'handlers': ['file'],
            'level': 'DEBUG',
        },
        'public': {
            'handlers': ['file'],
            'level': 'DEBUG',
        },
    }
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'

try:
    from local_settings import *
except ImportError, exp:
    pass
