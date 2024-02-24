"""
Django settings for paperswift_api project.

Generated by 'django-admin startproject' using Django 4.2.6.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-dyuqiy+@yi2%g+)ccujcf-uqnxs_(9uwgs*!6!*ht34o1!17sq"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['paperswiftsjcetest.pythonanywhere.com', '127.0.0.1']


# Application definition

INSTALLED_APPS = [
    # Django Admin Interface
    "admin_interface",
    "colorfield",
    # Django [REQUIRED]
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # CORS
    "corsheaders",
    # DRF
    'rest_framework',
    'rest_framework.authtoken',
    # Swagger Docs
    'drf_spectacular',
    # Django Allauth
    'allauth',
    'allauth.account',
    'dj_rest_auth',
    # Django OTP
    'django_otp',
    'django_otp.plugins.otp_totp',
    # Core Application
    'core'
]

# Django Admin Interface
X_FRAME_OPTIONS = "SAMEORIGIN"
SILENCED_SYSTEM_CHECKS = ["security.W019"]

SITE_ID = 1

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    # Django Allauth
    "allauth.account.middleware.AccountMiddleware",
    # Django OTP
    'django_otp.middleware.OTPMiddleware'
]

ROOT_URLCONF = "paperswift_api.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "paperswift_api.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Asia/Kolkata"

USE_I18N = True

USE_TZ = True

ROOT_URL = "http://127.0.0.1:8000"
STATIC_URL = "static/"
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
MEDIA_URL = 'media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
}


CORS_ALLOW_ALL_ORIGINS = True


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file_debug': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': './log/django.log',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'logger': {
            'handlers': ['file_debug'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
    'formatters': {
        'verbose': {
            'format': '%(asctime)s - %(levelname)s - %(message)s'
        },
    },
}