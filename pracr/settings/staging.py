from .base import *

DEBUG = False

ALLOWED_HOSTS = ['35.198.181.157',]





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
