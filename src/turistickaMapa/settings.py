# -*- coding: utf-8 -*-
"""
Django settings for turistickaMapa project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import logging
from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

TEMPLATE_CONTEXT_PROCESSORS += ("django.core.context_processors.request",)
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'y_)t%-hiypm3__0n!-4&1yepol*^6gkcwujiv7fddaffp$0^z%'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    "mapa",
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'turistickaMapa.urls'

WSGI_APPLICATION = 'turistickaMapa.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/turisti/static/'

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates'),
)
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/turisti/media/'

AUTH_PROFILE_MODULE = 'mapa.UserProfile'

STATICFILES_DIRS = ( 'static', )

#default database, will be included at server start...
default_layers = ["all"]
default_regions = u"Bratislavský Košický Trenčiansky Trnavský Prešovský Nitriansky Žilinský Banskobystrický Zahraničie".split()

logging.basicConfig(
  format = '%(asctime)s %(levelname)s %(message)s',
  filename = '/home/turisti/apache2logs/django.log',
  filemode = 'a'
)
