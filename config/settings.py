import os
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
APP_DIR = Path(getattr(sys, "_MEIPASS", BASE_DIR))
EXE_DIR = Path(sys.executable).resolve().parent if getattr(sys, "frozen", False) else BASE_DIR
SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret')
DEBUG = os.getenv('DEBUG', '0') == '1'
ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'apps.core',
    'apps.forms_registry',
    'apps.templates_engine',
    'apps.docgen',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'
TEMPLATES = [{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [BASE_DIR / 'templates'],
    'APP_DIRS': True,
    'OPTIONS': {'context_processors': [
        'django.template.context_processors.request',
        'django.contrib.auth.context_processors.auth',
        'django.contrib.messages.context_processors.messages',
    ]},
}]
WSGI_APPLICATION = 'config.wsgi.application'

db_engine = (os.getenv('DB_ENGINE') or '').strip().lower()
db_host = os.getenv('DB_HOST')

if db_engine in {'postgres', 'postgresql'} or db_host:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.getenv('DB_NAME', 'volopas_smk'),
            'USER': os.getenv('DB_USER') or os.getenv('USER', 'postgres'),
            'PASSWORD': os.getenv('DB_PASSWORD') or os.getenv('PASSWORD', '558955'),
            'HOST': db_host or '127.0.0.1',
            'PORT': os.getenv('DB_PORT', '5433'),
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.getenv('SQLITE_PATH', str(EXE_DIR / 'db.sqlite3')),
        }
    }

LANGUAGE_CODE = 'ru-ru'
TIME_ZONE = 'Europe/Moscow'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
STATICFILES_DIRS = [
    path for path in (
        APP_DIR / 'static',
        EXE_DIR / 'static',
        BASE_DIR / 'static',
    ) if path.exists()
]
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'storage'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
