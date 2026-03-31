from .base import *

DEBUG = False

ALLOWED_HOSTS = env.list(
    "ALLOWED_HOSTS",
    default=["ndiarama.com", "www.ndiarama.com"],
)

# CORS : à restreindre par env
CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOWED_ORIGINS = env.list("CORS_ALLOWED_ORIGINS", default=[])

# Sécurité
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