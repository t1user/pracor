from .base import *
from pracr.sendgrid_creds import *
from django.utils.log import DEFAULT_LOGGING

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'USER': 'tomek',
        'PASSWORD': 'Cookie123',
        'NAME': 'pracrdb',
        'HOST': 'localhost',
        'PORT': '',
    }
}

STATIC_URL = '/static/'

#admin docs
INSTALLED_APPS += [
    'django.contrib.admindocs',
    ]
MIDDLEWARE += [
    'django.contrib.admindocs.middleware.XViewMiddleware',
    ]
#end admin docs

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'django.server': DEFAULT_LOGGING['formatters']['django.server'],
        'verbose': {
            'format': '{levelname} {asctime} {name} line no: {lineno} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {name} {message}',
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
        'django.server': DEFAULT_LOGGING['handlers']['django.server'],
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler',
            'formatter': 'simple',
        },
        'console': {
            'level': 'DEBUG',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django.server': DEFAULT_LOGGING['loggers']['django.server'],
        'django': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'django.template': {
            'hanlders': ['console', ],
            'level': 'INFO', #DEBUG lists missing variables in admin, which is noisy
            'propagate': True,
            },
        'django.db.backends': {
            'level': 'ERROR',
            'handlers': ['console', ],
            'propagate': False,
        },
        'social_django': {
            'level': 'ERROR',
            'handlers': ['console', ],
            },
        'axes': {
            'level': 'ERROR',
            'handlers': ['console', ],
            },
        'reviews': {
            'level': 'DEBUG',
            'handlers': ['console', ],
            },
        'users': {
            'level': 'DEBUG',
            'handlers': ['console', ],
            },
    },
}


