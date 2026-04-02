#!/bin/bash
set -e

pip install -r requirements/base.txt
python manage.py collectstatic --noinput
python manage.py migrate

# Créer superuser automatiquement si les variables sont définies
if [ -n "$DJANGO_SUPERUSER_PASSWORD" ]; then
    python manage.py createsuperuser \
        --noinput \
        --username "${DJANGO_SUPERUSER_USERNAME:-admin}" \
        --email "${DJANGO_SUPERUSER_EMAIL:-admin@ndiarama.com}" \
        2>/dev/null || echo "Superuser existe deja"
fi