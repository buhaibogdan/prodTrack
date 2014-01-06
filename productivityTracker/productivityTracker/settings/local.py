"""
Django settings for productivityTracker project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""


from .base import *

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

POSTGRESQL_PASSWORD = get_env_variable("POSTGRESQL_PASSWORD")

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'prodTrack',
        'USER': 'postgres',
        'PASSWORD': POSTGRESQL_PASSWORD,
        'HOST': 'localhost',
        'PORT': 5432
    }
}

XS_SHARING_ALLOWED_ORIGINS = "*"

# --settings=productivityTracker.settings.local