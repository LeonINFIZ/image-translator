# src/config/settings/base.py
import os
from pathlib import Path

# BASE_DIR -> E:/Programming/Python/Text_recognition_in_images
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Local apps
    "translator.apps.TranslatorConfig",
    "common.apps.CommonConfig",  # Or "it_core.apps.ItCoreConfig" if you renamed it
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        # Corrected path: Look for templates in src/templates
        "DIRS": [BASE_DIR / "src" / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

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

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# Corrected paths: All paths should be relative to the project root (BASE_DIR)
GOOGLE_APPLICATION_CREDENTIALS = os.getenv(
    "GOOGLE_APPLICATION_CREDENTIALS",
    BASE_DIR / "poised-conduit-466006-c2-428db6f8af5e.json",
)
FONT_PATH = BASE_DIR / "arial.ttf"
TESSERACT_CMD = BASE_DIR / "Tesseract-OCR" / "tesseract.exe"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

LOGIN_URL = "translator:login"
LOGIN_REDIRECT_URL = "translator:translate"
LOGOUT_REDIRECT_URL = "translator:translate"
