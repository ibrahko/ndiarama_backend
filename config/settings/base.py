import os
from pathlib import Path

import environ
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

# --------------------------------------------------
# Chemins de base
# --------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# --------------------------------------------------
# Environnement
# --------------------------------------------------
env = environ.Env(
    DEBUG=(bool, False),
    SECRET_KEY=(str, "change-me-in-env"),
    ALLOWED_HOSTS=(list, []),
    DATABASE_URL=(str, "sqlite:///db.sqlite3"),
    SENTRY_DSN=(str, ""),
)

# Fichier .env optionnel a la racine du projet
env_file = BASE_DIR / "ndiarama_backend.env"
if env_file.exists():
    environ.Env.read_env(env_file)

DEBUG = env.bool("DEBUG")
SECRET_KEY = env("SECRET_KEY")
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=["*"])

# --------------------------------------------------
# Applications
# --------------------------------------------------
DJANGO_APPS = [
    # unfold DOIT etre avant django.contrib.admin
    "unfold",
    "unfold.contrib.filters",
    "unfold.contrib.forms",
    "unfold.contrib.inlines",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

THIRD_PARTY_APPS = [
    "rest_framework",
    "corsheaders",
    "django_filters",
    "drf_spectacular",
]

LOCAL_APPS = [
    "apps.core",
    "apps.mediaapp",
    "apps.services",
    "apps.community",
    "apps.communication",
    "apps.accounts",
    "apps.api",
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# --------------------------------------------------
# Middleware
# --------------------------------------------------
MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# --------------------------------------------------
# URLs / WSGI / ASGI
# --------------------------------------------------
ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.asgi.application"

# --------------------------------------------------
# Templates
# --------------------------------------------------
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

# --------------------------------------------------
# Base de donnees
# --------------------------------------------------
DATABASES = {
    "default": env.db("DATABASE_URL")
}

# --------------------------------------------------
# Auth / Passwords / Internationalisation
# --------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "fr-fr"
TIME_ZONE = "Africa/Bamako"
USE_I18N = True
USE_TZ = True

# --------------------------------------------------
# Static & Media
# --------------------------------------------------
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# --------------------------------------------------
# DRF / API
# --------------------------------------------------
REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.BasicAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.AllowAny",
    ],
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.SearchFilter",
        "rest_framework.filters.OrderingFilter",
    ],
    "DEFAULT_THROTTLE_CLASSES": [
        "rest_framework.throttling.AnonRateThrottle",
        "rest_framework.throttling.UserRateThrottle",
    ],
    "DEFAULT_THROTTLE_RATES": {
        "anon": "100/minute",
        "user": "1000/minute",
    },
}

SPECTACULAR_SETTINGS = {
    "TITLE": "NDIARAMA API",
    "DESCRIPTION": "API backend pour NDIARAMA Media & Consulting",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
}

# --------------------------------------------------
# CORS
# --------------------------------------------------
CORS_ALLOW_ALL_ORIGINS = env.bool("CORS_ALLOW_ALL_ORIGINS", default=True)
CORS_ALLOWED_ORIGINS = env.list("CORS_ALLOWED_ORIGINS", default=[])

# --------------------------------------------------
# Email
# --------------------------------------------------
DEFAULT_FROM_EMAIL = env("DEFAULT_FROM_EMAIL", default="no-reply@ndiarama.com")
CONTACT_EMAIL = env("CONTACT_EMAIL", default=DEFAULT_FROM_EMAIL)

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = env("EMAIL_HOST", default="")
EMAIL_PORT = env.int("EMAIL_PORT", default=587)
EMAIL_HOST_USER = env("EMAIL_HOST_USER", default="")
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD", default="")
EMAIL_USE_TLS = env.bool("EMAIL_USE_TLS", default=True)

# --------------------------------------------------
# Logging
# --------------------------------------------------
LOG_LEVEL = env("LOG_LEVEL", default="INFO")

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "[{levelname}] {asctime} {name} {process:d} {thread:d} {message}",
            "style": "{",
        },
        "simple": {
            "format": "[{levelname}] {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": LOG_LEVEL,
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": LOG_LEVEL,
            "propagate": True,
        },
        "django.request": {
            "handlers": ["console"],
            "level": "ERROR",
            "propagate": False,
        },
        "apps": {
            "handlers": ["console"],
            "level": LOG_LEVEL,
            "propagate": False,
        },
    },
}

# --------------------------------------------------
# Sentry (activable par env)
# --------------------------------------------------
SENTRY_DSN = env("SENTRY_DSN", default="")
if SENTRY_DSN:
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[DjangoIntegration()],
        traces_sample_rate=float(env("SENTRY_TRACES_SAMPLE_RATE", default="0.0")),
        send_default_pii=False,
    )

# --------------------------------------------------
# Securite generique
# --------------------------------------------------
CSRF_TRUSTED_ORIGINS = env.list("CSRF_TRUSTED_ORIGINS", default=[])
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTH_USER_MODEL = "accounts.User"

MAILCHIMP_API_KEY = env("MAILCHIMP_API_KEY", default="")
MAILCHIMP_LIST_ID = env("MAILCHIMP_LIST_ID", default="")
MAILCHIMP_SERVER_PREFIX = env("MAILCHIMP_SERVER_PREFIX", default="us16")
MAILCHIMP_REPLY_TO = env("MAILCHIMP_REPLY_TO", default="contact@ndiarama.com")

# --------------------------------------------------
# Admin CMS — django-unfold v0.98+ (oklch colors)
# --------------------------------------------------
UNFOLD = {
    "SITE_TITLE": "NDIARAMA",
    "SITE_HEADER": "NDIARAMA Media",
    "SITE_SUBHEADER": "Gestion du contenu",
    "SITE_URL": "/",
    "SITE_SYMBOL": "radio",
    "SHOW_HISTORY": True,
    "SHOW_VIEW_ON_SITE": False,
    "ENVIRONMENT": "config.settings.base.unfold_environment_callback",
    # Palette terracotta NDIARAMA en format oklch (requis par unfold v0.40+)
    "COLORS": {
        "primary": {
            "50":  "oklch(97.5% 0.010 52)",
            "100": "oklch(93.8% 0.025 52)",
            "200": "oklch(87.5% 0.050 52)",
            "300": "oklch(79.0% 0.080 52)",
            "400": "oklch(65.0% 0.110 52)",
            "500": "oklch(56.0% 0.115 50)",
            "600": "oklch(47.5% 0.110 48)",
            "700": "oklch(39.0% 0.095 46)",
            "800": "oklch(30.5% 0.075 44)",
            "900": "oklch(22.0% 0.050 42)",
            "950": "oklch(15.5% 0.030 38)",
        },
    },
    "SIDEBAR": {
        "show_search": True,
        "show_all_applications": False,
        "navigation": [
            {
                "title": "Contenu du site",
                "separator": True,
                "collapsible": False,
                "items": [
                    {
                        "title": "Parametres du site",
                        "icon": "settings",
                        "link": "/admin/core/sitesettings/",
                    },
                    {
                        "title": "Equipe",
                        "icon": "group",
                        "link": "/admin/core/teammember/",
                    },
                    {
                        "title": "Temoignages",
                        "icon": "format_quote",
                        "link": "/admin/core/testimonial/",
                    },
                ],
            },
            {
                "title": "Media",
                "separator": True,
                "collapsible": False,
                "items": [
                    {
                        "title": "Emissions",
                        "icon": "radio",
                        "link": "/admin/mediaapp/show/",
                    },
                    {
                        "title": "Episodes",
                        "icon": "play_circle",
                        "link": "/admin/mediaapp/episode/",
                    },
                ],
            },
            {
                "title": "Services",
                "separator": True,
                "collapsible": False,
                "items": [
                    {
                        "title": "Services & Formations",
                        "icon": "school",
                        "link": "/admin/services/service/",
                    },
                ],
            },
            {
                "title": "Communaute",
                "separator": True,
                "collapsible": False,
                "items": [
                    {
                        "title": "Programmes",
                        "icon": "emoji_events",
                        "link": "/admin/community/programhighlight/",
                    },
                    {
                        "title": "Avantages",
                        "icon": "diversity_3",
                        "link": "/admin/community/communityfeature/",
                    },
                    {
                        "title": "Posts sociaux",
                        "icon": "share",
                        "link": "/admin/community/socialpost/",
                    },
                ],
            },
            {
                "title": "Communications",
                "separator": True,
                "collapsible": False,
                "items": [
                    {
                        "title": "Messages recus",
                        "icon": "mail",
                        "link": "/admin/communication/contactmessage/",
                    },
                    {
                        "title": "Abonnes newsletter",
                        "icon": "group_add",
                        "link": "/admin/communication/newslettersubscriber/",
                    },
                ],
            },
            {
                "title": "Administration",
                "separator": True,
                "collapsible": True,
                "items": [
                    {
                        "title": "Utilisateurs",
                        "icon": "manage_accounts",
                        "link": "/admin/accounts/user/",
                    },
                ],
            },
        ],
    },
    "STYLES": ["/static/admin/css/ndiarama_admin.css"],
    "TABS": [],
}


def unfold_environment_callback(request):
    from django.conf import settings as _s
    if _s.DEBUG:
        return {"label": "Dev", "color": "orange"}
    return {"label": "Production", "color": "green"}
