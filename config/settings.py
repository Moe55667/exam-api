"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 4.2.13.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path

# env
from dotenv import load_dotenv
import os
load_dotenv()

secret_key = os.getenv('SECRET_KEY')
database_url = os.getenv('DATABASE_URL')
debug = os.getenv('DEBUG')


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = secret_key

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = debug

ALLOWED_HOSTS = ['127.0.0.1', 'localhost', 'exam-api.up.railway.app',]


# Application definition update

INSTALLED_APPS = [
    'corsheaders',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    "whitenoise.runserver_nostatic",#whitenoise
    'django.contrib.staticfiles',
    # third party apps
    'rest_framework',
    'rest_framework.authtoken',
    'djoser',
    'drf_spectacular',
    'django_filters',
    # local apps
    "api",
]


MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware', # Add CORS middleware here
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware", # whitenoise
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

CORS_ALLOWED_ORIGINS = [
    'https://exam-ui.up.railway.app',
    'http://localhost:5173'
]

CSRF_TRUSTED_ORIGINS = [
    'https://exam-api.up.railway.app',
    'https://exam-ui.up.railway.app',
    'http://localhost:5173'
]


REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticatedOrReadOnly",
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": [ 
        # auth for rest_browserable api 
        "rest_framework.authentication.SessionAuthentication",
        # auth for HTTPS api 
        "rest_framework.authentication.TokenAuthentication"
    ],  
}

DJOSER = {
    'USER_ID_FIELD': 'id',
    'LOGIN_FIELD': 'username',
    'SERIALIZERS': {
        'user': 'api.serializers.CustomUserSerializer',  # Use your custom serializer
        'current_user': 'api.serializers.CustomUserSerializer',
    },
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'Exam Ai',
    'DESCRIPTION': 'Automate Exams Using Ai',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
}



ROOT_URLCONF = 'config.urls'

# Import operating system library
import os

# Logging configuration

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,  # Keep Django's default loggers
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            # Log to a file
            'level': 'ERROR',  # Handle ERROR and above
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'django_errors.log'),  # Adjust the path as needed
            'formatter': 'verbose',  # Use the verbose formatter defined above
        },
        'console': {
            # Also log to console (useful for development)
            'level': 'INFO',  # Handle INFO and above
            'class': 'logging.StreamHandler',
            'formatter': 'simple',  # Use the simple formatter defined above
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file', 'console'],  # Use both file and console handlers
            'level': 'INFO',  # Adjust as needed
            'propagate': True,
        },
        # Define additional loggers for your own apps as needed
    },
}


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

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# RAILWAY POSTGRESQL DATABASE (LIVE)
# import dj_database_url
# DATABASES = {
#     'default': dj_database_url.parse(database_url)
# }


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'

STATICFILES_DIRS = [BASE_DIR / "static"] # new
STATIC_ROOT = BASE_DIR / "staticfiles" # new
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage" # new


MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


