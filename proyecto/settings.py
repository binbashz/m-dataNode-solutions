import os  
from pathlib import Path
from django.urls import reverse_lazy
from decouple import config
from dotenv import load_dotenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# Secret key

SECRET_KEY = config('SECRET_KEY')

CSRF_TRUSTED_ORIGINS = [
    'https://cannatech.onrender.com',
    'http://localhost',
    'https://127.0.0.1',
    'http://127.0.0.1',
    'https://127.0.0.1:8000'
]


ALLOWED_HOSTS = [
    'cannatech.onrender.com', 
    'localhost', 
    '127.0.0.1',
    'https://127.0.0.1:8000',
    'http://127.0.0.1:8000',
    'web'
]

# http://127.0.0.1:8000/ en navegador

DEBUG = config('DEBUG', default=False, cast=bool)  #  DEBUG estar en False para producción

# Security settings for production
SECURE_SSL_REDIRECT = not DEBUG
CSRF_COOKIE_SECURE = not DEBUG
SESSION_COOKIE_SECURE = not DEBUG
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https') if not DEBUG else None

LOGIN_REDIRECT_URL = reverse_lazy('home')

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_apscheduler',
    'core',
    'rest_framework',
]

APSCHEDULER_DATETIME_FORMAT = "N j, Y, f:s a"
APSCHEDULER_RUN_NOW_TIMEOUT = 25  # Segundos

AUTH_USER_MODEL = 'auth.User'
DATE_INPUT_FORMATS = ('%d/%m/%Y','%Y-%m-%d', '%d-%m-%Y')

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.common.BrokenLinkEmailsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

SCHEDULER_AUTOSTART = True

ROOT_URLCONF = 'proyecto.urls'

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
                'django.contrib.messages.context_processors.messages'
            ],
        },
    },
]

load_dotenv()  # Carga las variables de entorno desde el archivo .env

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('PGDATABASE'),
        'USER': os.getenv('PGUSER'),
        'PASSWORD': os.getenv('PGPASSWORD'),
        'HOST': os.getenv('PGHOST'),
        'PORT': os.getenv('PGPORT', 5432),
        'OPTIONS': {
            'sslmode': 'require',
        },
    }
}

print("Database:", os.getenv('PGDATABASE'))
print("User:", os.getenv('PGUSER'))

WSGI_APPLICATION = 'proyecto.wsgi.application'

# Password validation
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

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'



# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'America/Montevideo'
USE_TZ = True
USE_I18N = True
USE_L10N = False

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Error pages
handler404 = 'core.views.error_page'
handler500 = 'core.views.error_page'
