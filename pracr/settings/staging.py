from .base import *
from pracr.sendgrid_key import SENDGRID_API_KEY
import sys, os

DEBUG = False


ALLOWED_HOSTS = ['35.198.181.157',
                 'www.pracor.pl',
                 'pracor.pl',
                 '157.181.198.35.bc.googleusercontent.com',]



# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'USER': 'tomek',
        'PASSWORD': 'Cookie123',
        'NAME': 'pracr',
        'HOST': 'localhost',
        'PORT': '',
    }
}
STATIC_URL = '/static_root/'

EMAIL_BACKEND = 'sendgrid_backend.SendgridBackend'
SENDGRID_SANDBOX_MODE_IN_DEBUG = False

#required by debug_toolbars
INTERNAL_IPS += ['89.73.79.21', '']

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}

SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True


LOG_ROOT = os.path.join(os.path.dirname(BASE_DIR), 'log')
HANDLERS_LIST = ['mail_admins', 'rotating_file', 'day_rotating_file']
LOGLEVEL = os.environ.get('PRACOR_LOGLEVEL', 'ERROR').upper()
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{asctime} {module} {levelname} {message}',
            'style': '{',
        },
    },
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'stream': sys.stdout,
            'formatter': 'simple'
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'debug.log',
            'formatter': 'simple',
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler',
            'formatter': 'simple',
        },
        'rotating_file': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOG_ROOT, 'error.log'),
            'maxBytes': 1024*1024*15, # 15MB
            'backupCount': 10,
            'formatter': 'simple',
        },
        'day_rotating_file': {
            'level': 'INFO',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.join(LOG_ROOT, 'info.log'),
            'when': 'D',
            'backupCount': 30,
            'formatter': 'simple',
            },
    },
    'loggers': {
        'django': {
            'handlers': HANDLERS_LIST,
            'level': 'DEBUG',
            'propagate': True,
        },
        'django.template': {
            'level': 'NOTSET',
            'propagate': False,
            },
        'axes': {
            'handlers': HANDLERS_LIST,
            'level': 'ERROR',
            'propagate': True,
        },
        'social_django': {
            'handlers': HANDLERS_LIST,
            'level': 'DEBUG',
            'propagate': True,
        },
        'reviews': {
            'handlers': HANDLERS_LIST,
            'level': 'DEBUG',
            'propagate': True,
            },
        'users': {
            'handlers': HANDLERS_LIST,
            'level': 'DEBUG',
            'propagate': True,
            },
    },
}
