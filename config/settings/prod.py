from django.core.exceptions import ImproperlyConfigured

from .base import *

DEBUG = False

# ── Fail-fast : refuse de démarrer sans configuration sûre ──
if not SECRET_KEY or SECRET_KEY.startswith(("change-me", "django-insecure")):
    raise ImproperlyConfigured(
        "SECRET_KEY manquante ou non sécurisée. "
        "Définissez la variable d'environnement SECRET_KEY en production."
    )

if not CLOUDINARY_URL:
    import logging
    logging.getLogger(__name__).warning(
        "CLOUDINARY_URL non définie : les fichiers média sont stockés sur le "
        "disque local (éphémère sur Railway — perdus à chaque redéploiement)."
    )

ALLOWED_HOSTS = env.list(
    "ALLOWED_HOSTS",
    default=["ndiarama.com", "www.ndiarama.com"],
)

# CORS : à restreindre par env
CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOWED_ORIGINS = env.list("CORS_ALLOWED_ORIGINS", default=[
    "https://ndiarama-front.vercel.app",
])
CORS_ALLOW_HEADERS = [
    "accept",
    "accept-encoding",
    "authorization",
    "content-type",
    "dnt",
    "origin",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
]

# Static files — /tmp est toujours accessible en ecriture sur Railway
STATIC_ROOT = "/tmp/staticfiles"

# Securite
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = env.int("SECURE_HSTS_SECONDS", default=3600)
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_SSL_REDIRECT = env.bool("SECURE_SSL_REDIRECT", default=True)

# Email réel (paramétré via variables d'environnement)
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

# Logging prod : niveau INFO par défaut
LOG_LEVEL = env("LOG_LEVEL", default="INFO")
for logger_name in ["django", "apps", "django.request"]:
    LOGGING["loggers"][logger_name]["level"] = LOG_LEVEL
LOGGING["root"]["level"] = LOG_LEVEL