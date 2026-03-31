from .base import *

DEBUG = True

ALLOWED_HOSTS = ["*"]

# CORS très permissif en dev
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOWED_ORIGINS = []

# Email en console
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# Logging plus verbeux en dev
LOG_LEVEL = "DEBUG"
for logger_name in ["django", "apps", "django.request"]:
    LOGGING["loggers"][logger_name]["level"] = LOG_LEVEL
LOGGING["root"]["level"] = LOG_LEVEL