import os
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent


def get_env(name, default=None, required=False):
    value = os.environ.get(name, default)
    if required and not value:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value


def get_bool_env(name, default=False):
    return get_env(name, str(default)).lower() in {'1', 'true', 'yes', 'on'}


SECRET_KEY = get_env('SECRET_KEY', required=True)
DEBUG = get_bool_env('DEBUG', default=False)
ALLOWED_HOSTS = [
    host.strip()
    for host in get_env('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')
    if host.strip()
]


INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'proveedor_app',
    'widget_tweaks',
    'django.contrib.humanize',
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

ROOT_URLCONF = 'proveedor.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'proveedor_app' / 'templates' / 'proveedor'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'proveedor.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': get_env('DB_NAME', required=True),
        'USER': get_env('DB_USER', required=True),
        'PASSWORD': get_env('DB_PASS', required=True),
        'HOST': get_env('DB_HOST', default='db'),
        'PORT': get_env('DB_PORT', default='3306'),
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}


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


LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

LOGIN_REDIRECT_URL = '/inicio/'
LOGOUT_REDIRECT_URL = '/login/'
LOGIN_URL = '/login/'

SESSION_COOKIE_AGE = 1800
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_ENGINE = 'django.contrib.sessions.backends.db'


STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'
