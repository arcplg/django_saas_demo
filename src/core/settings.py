"""
Django settings for cfehome project.

Generated by 'django-admin startproject' using Django 5.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""
import os
from pathlib import Path
from decouple import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Email config
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = config("EMAIL_HOST", cast=str, default="smtp.gmail.com")
EMAIL_PORT = config("EMAIL_PORT", cast=str, default="587") # Recommended
EMAIL_HOST_USER = config("EMAIL_HOST_USER", cast=str, default=None)
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD", cast=str, default=None)
EMAIL_USE_TLS = config("EMAIL_USE_TLS", cast=bool, default=True)  # Use EMAIL_PORT 587 for TLS
EMAIL_USE_SSL = config("EMAIL_USE_SSL", cast=bool, default=False)  # Use MAIL_PORT 465 for SSL
print(EMAIL_USE_TLS, EMAIL_USE_SSL)

ADMINS=[('TrieuNB', 'trieuconcrete@concrete-corp.com')]
MANAGERS=ADMINS

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY")
SECRET_KEY = config("DJANGO_SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = str(os.environ.get('DJANGO_DEBUG')).lower() == "true"
DEBUG = config("DJANGO_DEBUG", cast=bool)

print("DEBUG", DEBUG, type(DEBUG))

ALLOWED_HOSTS = [
    ".railway.app" # https://saas.prod.railway.app
]
if DEBUG:
    ALLOWED_HOSTS += [
        "127.0.0.1",
        "localhost"
    ]

# Application definition

INSTALLED_APPS = [
    # django apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # apps
    'apps.visits',
    'apps.commando',
    'apps.demo',
    'apps.profiles',
    # third-party-apps
    'allauth',
    'allauth.account',
    # Optional -- requires install using `django-allauth[socialaccount]`.
    'allauth.socialaccount',
    'allauth_ui',
    'widget_tweaks',
    'slippers',
    'allauth.socialaccount.providers.github',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # Add the account middleware:
    "allauth.account.middleware.AccountMiddleware",
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"],
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
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        "NAME": config("MYSQL_DATABASE", default="django"),
        "USER": config("MYSQL_USER", default="user"),
        "PASSWORD": config("MYSQL_PASSWORD", default="password"),
        "HOST": config("MYSQL_HOST", default="127.0.0.1"),
        "PORT": config("MYSQL_PORT", default="3306"),
        "OPTIONS": {
            "init_command": "SET sql_mode='STRICT_TRANS_TABLES'" 
        }
    }
}

CONN_MAX_AGE = config("CONN_MAX_AGE", cast=str, default=30)
DATABASE_URL = config("DATABASE_URL", default=None)

if DATABASE_URL is not None:
    import dj_database_url
    DATABASES = {
        "default": dj_database_url.config(
            default=DATABASE_URL,
            conn_max_age=30,
            conn_health_checks=True
        )
    }

# Add these at the top of your settings.py
# from os import getenv
# from dotenv import load_dotenv

# Replace the DATABASES section of your settings.py with this
# tmpPostgres = urlparse(os.getenv("DATABASE_URL"))

# DATABASES = {
#   'default': {
#     'ENGINE': 'django.db.backends.postgresql',
#     'NAME': config('PGDATABASE'),
#     'USER': config('PGUSER'),
#     'PASSWORD': config('PGPASSWORD'),
#     'HOST': config('PGHOST'),
#     'PORT': config('PGPORT', 5432),
#     'OPTIONS': {
#       'sslmode': 'require',
#     },
#   }
# }

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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

LOGIN_REDIRECT_URL = "/"
ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
ACCOUNT_EMAIL_SUBJECT_PREFIX = "[DJANGO SaaS] "

# Django Allauth Config
AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by email
    'allauth.account.auth_backends.AuthenticationBackend',
]

# Provider specific settings
SOCIALACCOUNT_PROVIDERS = {
    'github': {
        'VERIFIED_EMAIL': True
        # 'SCOPE': [
        #     'user',
        #     'repo',
        #     'read:org',
        # ],
    }
}

# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'
STATICFILES_BASE_DIRS = BASE_DIR / "staticfiles"
STATICFILES_BASE_DIRS.mkdir(exist_ok=True, parents=True)
STATICFILES_ASSETS_DIR = STATICFILES_BASE_DIRS / "assets"

# source for python manage.py collectstatic

STATICFILES_DIRS = [
    STATICFILES_BASE_DIRS
]

# output for python manage.py collectstatic
# local cdn
# STATIC_ROOT = BASE_DIR.parent / "local-cdn"
STATIC_ROOT = BASE_DIR / "local-cdn" # generate in src dir

# < Django 4.2
# STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
