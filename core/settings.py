"""
Django settings for bahoo_backend project.

Generated by 'django-admin startproject' using Django 4.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""
import logging.config
from datetime import timedelta
from pathlib import Path

from corsheaders.defaults import default_headers, default_methods
from smart_getenv import getenv
from dotenv import load_dotenv

load_dotenv('.env', override=True)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/
DEBUG = getenv('DEBUG', type=bool, default=True)

SECRET_KEY = getenv(
    'SECRET_KEY',
    default='django-insecure-&_gv#ftaza)hq7l9*g44mz4*gkqc7x7qr$ewz5hhr1b1r8ic$m',
)

ALLOWED_HOSTS = getenv('ALLOWED_HOSTS', type=list, default=['*'])

GHASEDAK_API_KEY = getenv('GHASEDAK_API_KEY', type=str)
OTP_EXPIRE_TIME = getenv('OTP_EXPIRE_TIME', type=int, default=5*60)
OTP_TEMPLATE_NAME = getenv('OTP_TEMPLATE_NAME', default='BahooVerification1')


# Application definition
APP_VERSION = '1.0.0'
APP_NAME = 'bahoo'
APP_DESCRIPTION = 'RESTfull API backend for Bahoo service'

MY_APPS = [
    'api',
    'api.users',
    'api.authentication',
    'api.invoice',
    'api.tag',
    'api.reminder',
    'api.transaction',
]

INSTALLED_APPS = [
    'rest_framework',
    'corsheaders',
    'phonenumber_field',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
] + MY_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

LOGIN_URL = '/auth/login/'

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'core.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': getenv('DB_NAME', default='bahoodb'),
        'USER': getenv('DB_USER'),
        'PASSWORD': getenv('DB_PASSWORD'),
        'HOST': getenv('DB_HOST'),
        'PORT': getenv('DB_PORT'),
        'CONN_MAX_AGE': getenv('DB_CONN_MAX_AGE', type=int, default=0),
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

AUTH_USER_MODEL = 'users.User'


# Logging configuration
# https://docs.djangoproject.com/en/4.0/topics/logging/#configuring-logging

LOGGING_CONFIG = None  # This empties out Django's logging config
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'formatters': {
        'verbose': {
            'format': '%(asctime)s %(levelname)s module=%(module)s, '
            'process_id=%(process)d, %(message)s'
        }
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
        'celery': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}

logging.config.dictConfig(LOGGING)


# django-cors-headers
# https://pypi.org/project/django-cors-headers/

CORS_ORIGIN_ALLOW_ALL = getenv('CORS_ORIGIN_ALLOW_ALL', type=bool, default=True)
CORS_ALLOWED_ORIGINS = getenv('CORS_ALLOWED_ORIGINS', type=list, default=[])
CORS_ALLOW_HEADERS = getenv(
    'CORS_ALLOW_HEADERS', type=list, default=list(default_headers)
)
CORS_ALLOW_METHODS = getenv(
    'CORS_ALLOW_METHODS', type=list, default=list(default_methods)
)


# Rest Framework
# https://www.django-rest-framework.org/api-guide/settings/#settings
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'core.renderer.BahooRenderer',
    ),
    'EXCEPTION_HANDLER':'core.exception_handler.bahoo_exception_handler',
}


# Simple JWT
# https://django-rest-framework-simplejwt.readthedocs.io/en/latest/settings.html
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=30),
    'UPDATE_LAST_LOGIN': True,
}


# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = getenv('TIME_ZONE', default='UTC')

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
