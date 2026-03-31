FROM python:3.12-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libpq-dev \
 && rm -rf /var/lib/apt/lists/*

COPY requirements/ /app/requirements/
RUN pip install --upgrade pip \
 && pip install -r requirements/prod.txt

COPY . /app

RUN useradd -ms /bin/bash appuser
USER appuser

ENV DJANGO_SETTINGS_MODULE=config.settings.prod

CMD ["gunicorn", "config.wsgi:application", "-w", "4", "-b", "0.0.0.0:8000"]