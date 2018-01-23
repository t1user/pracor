from .base import *
from pracr.sendgrid_key import SENDGRID_API_KEY

DEBUG = False


ALLOWED_HOSTS = ['35.198.181.157',]



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

"""
LOG_ROOT = os.path.join(os.path.dirname(BASE_DIR), 'log')
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'applogfile': {
            'level':'DEBUG',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOG_ROOT, 'pracr.log'),
            'maxBytes': 1024*1024*15, # 15MB
            'backupCount': 10,
        },
    },
    'loggers': {
        'django': {
            'handlers': ['mail_admins', 'applogfile'],
            'level': 'ERROR',
            'propagate': True,
        },
        'social_django': {
            'handlers': ['applogfile',],
            'level': 'DEBUG',
        },
    },
}
"""

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'debug.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}



EMAIL_BACKEND = 'sendgrid_backend.SendgridBackend'
SENDGRID_SANDBOX_MODE_IN_DEBUG = False

#required by debug_toolbars
INSTALLED_APPS += [
    'debug_toolbar',
    ]

MIDDLEWARE += [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    ]

INTERNAL_IPS = ['127.0.0.1', '89.73.79.21']
#end required by debug_toolbars
