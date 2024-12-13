import os

from pracor.facebook_creds import *
from pracor.google_creds import *
from pracor.linkedin_config import *

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from pracor.secret_key import SECRET_KEY
except ImportError:
    from pracor.generate_secret_key import generate

    generate()
    from pracor.secret_key import SECRET_KEY  # noqa


DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.postgres",
    "django.contrib.humanize",
    "django.contrib.sites",
    "django.contrib.sitemaps",
]

THIRD_PARTY_APPS = [
    "social_django",
    "axes",
    "debug_toolbar",
    "analytical",
    # "admin_honeypot",
]

PROJECT_APPS = [
    "users",
    "reviews",
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + PROJECT_APPS

SITE_ID = 1

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.middleware.common.BrokenLinkEmailsMiddleware",
    "social_django.middleware.SocialAuthExceptionMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "axes.middleware.AxesMiddleware",
]

ROOT_URLCONF = "pracor.urls"

AUTHENTICATION_BACKENDS = (
    "social_core.backends.linkedin.LinkedinOAuth2",
    "social_core.backends.google.GoogleOAuth2",
    "social_core.backends.facebook.FacebookOAuth2",
    "django.contrib.auth.backends.ModelBackend",
    "axes.backends.AxesStandaloneBackend",
)


TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "social_django.context_processors.backends",
                "social_django.context_processors.login_redirect",
            ],
        },
    },
]

WSGI_APPLICATION = "pracor.wsgi.application"


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
    "django.contrib.auth.hashers.BCryptPasswordHasher",
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.Argon2PasswordHasher",
]

AUTH_USER_MODEL = "users.User"

LANGUAGE_CODE = "pl"

TIME_ZONE = "Europe/Warsaw"

USE_I18N = True

USE_L10N = True

USE_TZ = True


STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]
STATIC_ROOT = os.path.join(BASE_DIR, "static_root")

LOGIN_URL = "login"
LOGIN_REDIRECT_URL = "home"
LOGOUT_REDIRECT_URL = "logged_out"


ADMINS = [("Tom", "tomasz2605@gmail.com"), ("Group Admin", "admin@pracor.pl")]
MANAGERS = ADMINS
EMAILS_USE_LOCALTIME = True
SERVER_EMAIL = "admin@pracor.pl"
DEFAULT_FROM_EMAIL = "admin@pracor.pl"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# used in views to specify to whom contact info should be sent
CONTACT_EMAILS = ["tomasz2605@gmail.com", "kontakt@pracor.pl"]

# required by debug toolbars
INTERNAL_IPS = [
    "127.0.0.1",
]

# axes configuration
AXES_FAILURE_LIMIT = 5
AXES_COOLOFF_TIME = 1  # hour
# template to render when a user is locked out. Template receives cooloff_time and failure_limit as context variables.
AXES_LOCKOUT_TEMPLATE = "registration/wrong_password_block.html"
# AXES_LOCOUT_URL = #specifies a URL to redirect to on lockout. If both AXES_LOCKOUT_TEMPLATE and AXES_LOCKOUT_URL are set, the template will be used.
# AXES_ONLY_USER_FAILURES = False

# django_analytical configuration
CLICKY_SITE_ID = "101101103"
GOOGLE_ANALYTICS_PROPERTY_ID = "UA-112817315-1"
GOOGLE_ANALYTICS_SITE_SPEED = True
ANALYTICAL_INTERNAL_IPS = []
