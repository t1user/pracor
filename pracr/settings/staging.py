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
        'NAME': 'pracr',
        'HOST': 'localhost',
        'PORT': '',
    }
}

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static_root"),
]
STATIC_ROOT = os.path.join(BASE_DIR, 'static_root')
