from django.db import models


class ProgramHighlight(models.Model):
    """Programmes mis en avant : Chevening, YALI, etc."""

    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    short_description = models.CharField(max_length=500, blank=True)
    external_link = models.URLField(blank=True)

    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["order", "name"]

    def __str__(self):
        return self.name


class CommunityFeature(models.Model):
    """Fiches descriptives de la communauté / avantages."""

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    telegram_link = models.URLField(
        blank=True,
        help_text="Lien vers le groupe Telegram privé.",
    )
    show_newsletter_button = models.BooleanField(default=True)

    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["order", "title"]

    def __str__(self):
        return self.title