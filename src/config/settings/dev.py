from config.settings.base import *

SECRET_KEY = "django-insecure-7rk)yxw7=uyftasz0b&9^ez)6$isnsznedn2l(f%!rs$7gdef$"

DEBUG = True
ALLOWED_HOSTS = []

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",  # db.sqlite3 буде в корені проєкту
    }
}

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR.parent / "media"

STATIC_URL = "static/"
STATICFILES_DIRS = [
    BASE_DIR.parent / "static",
]