from config.settings.base import *  # NOQA:F403

SECRET_KEY = "django-insecure-7rk)yxw7=uyftasz0b&9^ez)6$isnsznedn2l(f%!rs$7gdef$"

DEBUG = True

ALLOWED_HOSTS = ["*"]

INSTALLED_APPS += [
    "django_extensions",
    "debug_toolbar",
]


MIDDLEWARE += [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
]


INTERNAL_IPS = [
    "127.0.0.1",
]


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

STATIC_URL = "static/"
STATICFILES_DIRS = [
    BASE_DIR / "static",
]
