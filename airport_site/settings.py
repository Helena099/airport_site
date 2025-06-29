from pathlib import Path
import os
from dotenv import load_dotenv
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "dev-key")
DEBUG = True
ALLOWED_HOSTS = []

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "airport",
]

INSTALLED_APPS += ["rest_framework"]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "airport_site.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "airport_site.wsgi.application"

# DATABASES = {
#     "default": {
#         "ENGINE": "djongo",
#         "NAME": "airport",
#         "ENFORCE_SCHEMA": False,
#         "CLIENT": {
#             "host": os.getenv("MONGO_URI"),
#         },
#     }
# }

DATABASES = {
    "default": {                       # SQLite pour tout ce que Django génère
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    },
    "mongo": {                         # Djongo, uniquement pour l’app airport
        "ENGINE": "djongo",
        "NAME": "airport",
        "ENFORCE_SCHEMA": False,
        "CLIENT": {
            "host": os.getenv("MONGO_URI", "mongodb://localhost:27017/"),
        },
    },
}

DATABASE_ROUTERS = ["airport.routers.MongoRouter"]


# Email backend
# EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv("EMAIL_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_PASS")
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

LANGUAGE_CODE = "fr-fr"
TIME_ZONE = "Europe/Paris"
USE_I18N = True
USE_TZ = True

STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
