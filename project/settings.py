import os
from pathlib import Path
from decouple import config
from datetime import timedelta

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY', default='django-insecure-$!@#^*&%^!@#*^&*!%$#@$^%!^@$')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=True, cast=bool)

ALLOWED_HOSTS = [
    "*"
]


# Application definition

INSTALLED_APPS = [
    # django unfold theme 
    "unfold",
    "unfold.contrib.filters",
    "unfold.contrib.forms",
    "unfold.contrib.inlines",
    "unfold.contrib.import_export",
    "unfold.contrib.guardian",
    "unfold.contrib.simple_history",
    "unfold.contrib.location_field",
    # default apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # 3rd party

    # lcoal apps
    'apps.account',
    'apps.core',
    'apps.dashboard',
    'apps.socialauth',
    'apps.website',

]


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 3rd party middleware

    # custom middleware
]

ROOT_URLCONF = 'project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR/'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # custom context processors
                'apps.core.context_processors.site_settings',
            ],
        },
    },
]

WSGI_APPLICATION = 'project.wsgi.application'

# for asgi
# ASGI_APPLICATION = 'project.asgi.application'



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


# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


###################################
#             DATABASE            #
###################################
from .conf import database
DATABASES = database.SQLITE


# CONSOLE EMAIL BACKEND
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend' # use in development only

#################### SMTP EMAIL BACKEND ######################
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = config('EMAIL_HOST', default='localhost')
# EMAIL_PORT = config('EMAIL_PORT', default=25)
# EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')
# EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')
# EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=False, cast=bool)

###################################
#         STATIC FILES            #
###################################

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR/'static',
]
STATIC_ROOT = BASE_DIR/'staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR/'media'

# Default file storage
DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

###################################
#                DRF              #
###################################

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',        
    ],
    # 'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    # 'PAGE_SIZE': 10,
    'EXCEPTION_HANDLER': 'project.custom_exception.custom_exception_handler',

}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=30),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': True,
}

# Custom User Model
AUTH_USER_MODEL = 'account.User'



