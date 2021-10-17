"""
Django settings for BaseDjangoProject project.

Generated by 'django-admin startproject' using Django 3.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""
import os

import mimetypes
mimetypes.add_type("text/css", ".css", True)

from pathlib import Path
import mimetypes
import environ
from . import database

env = environ.Env()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


env.read_env(os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = database.get_env_variable('SECRET_KEY', default="yei_155kav0$heys#74bbyg(ra196&hzock3o6i1im5c6e_do") #'yei_155kav0$heys#74bbyg(ra196&hzock3o6i1im5c6e_do)'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
DEBUG_PROPAGATE_EXCEPTIONS = True
ALLOWED_HOSTS = [
    'construction-market.herokuapp.com',
    '127.0.0.1'
]


# Application definition

INSTALLED_APPS = [

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    #'django.contrib.staticfiles',
    'django.contrib.sites',  # <<<

    'crispy_forms',
    'todo',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    "the_system",
    'admin_honeypot',
    'rest_framework',
    'django_otp',
    'django_otp.plugins.otp_totp',
    'the_todo',
    'the_user',

    'pinax.messages',
    'the_messages',  # extension to pinax.messages

    'the_activity',
    'rosetta',
    'SampleApp',
]


CRISPY_TEMPLATE_PACK = 'bootstrap4'

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'
# -----------------------------------------------------------------------------------


SITE_ID = 1

# -----------------------------------------------------------------------------------

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',  # locale middleware must be between Session and Common

    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django_otp.middleware.OTPMiddleware',  # google auth

    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',


    'the_activity.middleware.ActivityMiddleware',
    'the_system.middleware.TheSystemMiddleware',

    'whitenoise.middleware.WhiteNoiseMiddleware',

]

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

ROOT_URLCONF = 'BaseDjangoProject.urls'

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
                'the_system.context_processor.SystemConfigContextProcessor',  ## <<<
                'the_activity.context_processor.user_activity_context_processor',

                'django.template.context_processors.static',
                "pinax.messages.context_processors.user_messages",

                'the_todo.context_processor.to_do_context_processor',
            ],
        },
    },
]

WSGI_APPLICATION = 'BaseDjangoProject.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': database.config(),
    #'iseries': database.ibmi(),
}


# -----------------------------------------------------------------------------------
#  DATABASE_ROUTERS : defines is app need to use a specific database
# -----------------------------------------------------------------------------------
DATABASE_ROUTERS = [
   # 'SampleApp.db_routers.KWBD108Router',
             ]

# -----------------------------------------------------------------------------------
#
# -----------------------------------------------------------------------------------

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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

# -----------------------------------------------------------------------------------
# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/
# -----------------------------------------------------------------------------------

LANGUAGE_CODE = database.get_env_variable('LANGUAGE_CODE', default='en-us')

from django.utils.translation import gettext_lazy as _

#supported languages
LANGUAGES = (
    ('en', _('English')),
    ('hi', _('Hindi')),
)

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale/'),
)


TIME_ZONE = database.get_env_variable('TIME_ZONE', default='US/Central')

USE_I18N = True

USE_L10N = True

USE_TZ = True


# -----------------------------------------------------------------------------------
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/
# -----------------------------------------------------------------------------------

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

# The STATICFILES_DIRS setting should not contain the STATIC_ROOT setting.

# STATICFILES_DIRS = [
#     # os.path.join(BASE_DIR, 'static'),
#
#     # os.path.join(BASE_DIR, 'static'),
#     # os.path.join(BASE_DIR, 'tasks')
# ]

# -------------------------------------------------------------
#  Login
# -------------------------------------------------------------

# sumit > go to this url after login
LOGIN_REDIRECT_URL = "/"

# LOGOUT_REDIRECT_URL = "/account_login/"

# ------------------------------------------------------
#
# ------------------------------------------------------
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'mediax')
# ------------------------------------------------------
#
# ------------------------------------------------------
mimetypes.add_type("image/svg+xml", ".svg", True)
mimetypes.add_type("image/svg+xml", ".svgz", True)
# ------------------------------------------------------
# django-otp
# ------------------------------------------------------
OTP_TOTP_ISSUER = 'BaseDjangoProject'
OTP_ENTRY_URL = '/user/twofactor/'

# -------------------------------------------------------------
#
# -------------------------------------------------------------
JWT_SECRET = database.get_env_variable('JWT_SECRET')

# -------------------------------------------------------------
# django-allauth registraion settings
# -------------------------------------------------------------
# https://dev.to/gajesh/the-complete-django-allauth-guide-la3
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 1
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = "optional"
ACCOUNT_LOGIN_ATTEMPTS_LIMIT = 5

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        # For each OAuth based provider, either add a ``SocialApp``
        # (``socialaccount`` app) containing the required client
        # credentials, or list them here:
        'APP': {
            'client_id': '123',
            'secret': '456',
            'key': ''
        }
    }
}

# ACCOUNT_FORMS = {'signup': 'the_user.forms.SignupFormWithGroup'} #PaysaPlus
# -------------------------------------------------------------




# -------------------------------------------------------------
# TO send emails
# -------------------------------------------------------------


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = database.get_env_variable('EMAIL_HOST', default='smtp.gmail.com')
EMAIL_USE_TLS = database.get_env_variable('EMAIL_USE_TLS', default=True)
EMAIL_PORT = database.get_env_variable('EMAIL_PORT', default=587)
EMAIL_HOST_USER = database.get_env_variable('EMAIL_HOST_USER', default='onlysumitg@gmail.com')
EMAIL_HOST_PASSWORD = database.get_env_variable('EMAIL_HOST_PASSWORD', default="")

# -------------------------------------------------------------
#  for encrypted fields
# -------------------------------------------------------------
# https://django-fernet-fields.readthedocs.io/en/latest/
FERNET_KEYS = [
    os.environ.get('FIELD_ENCRYPTION_KEY', 'ZpoI-PByJfCVY4Kr4cqrQbJcDBLQgE9VnGIhhgqxFec='),
    '',
    # 'older key for decrypting old data',
]

# -------------------------------------------------------------
#  list past size
# -------------------------------------------------------------
PAGE_SIZE = 25

# -------------------------------------------------------------
#
# -------------------------------------------------------------
# Uncomment this to print all SQLs
# LOGGING = {
#     'version': 1,
#     'filters': {
#         'require_debug_true': {
#             '()': 'django.utils.log.RequireDebugTrue',
#         }
#     },
#     'handlers': {
#         'console': {
#             'level': 'DEBUG',
#             'filters': ['require_debug_true'],
#             'class': 'logging.StreamHandler',
#         }
#     },
#     'loggers': {
#         'django.db.backends': {
#             'level': 'DEBUG',
#             'handlers': ['console'],
#         }
#     }
# }