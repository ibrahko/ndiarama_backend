"""
Modeles de l'application community.
"""
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
    """Fiches descriptives de la communaute / avantages."""

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    telegram_link = models.URLField(
        blank=True,
        help_text="Lien vers le groupe Telegram prive.",
    )
    show_newsletter_button = models.BooleanField(default=True)

    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["order", "title"]

    def __str__(self):
        return self.title


class SocialPost(models.Model):
    """
    Post reseaux sociaux a afficher dans SocialFeedPreview.
    Gere depuis l'admin Django — plus besoin de modifier le code front.
    Ref CDC : "Apercu des derniers posts LinkedIn & TikTok".
    """

    PLATFORM_LINKEDIN = "linkedin"
    PLATFORM_TIKTOK   = "tiktok"
    PLATFORM_CHOICES  = (
        (PLATFORM_LINKEDIN, "LinkedIn"),
        (PLATFORM_TIKTOK,   "TikTok"),
    )

    platform = models.CharField(
        max_length=20,
        choices=PLATFORM_CHOICES,
        help_text="Reseau social du post.",
    )
    excerpt = models.TextField(
        help_text="Texte court du post (2-3 lignes max, affiche en front).",
    )
    url = models.URLField(
        help_text="Lien direct vers le post ou vers le profil.",
    )
    published_at = models.DateField(
        help_text="Date de publication du post.",
    )
    likes = models.PositiveIntegerField(
        default=0,
        help_text="Nombre de j'aime approximatif (mis a jour manuellement).",
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Decocher pour masquer ce post sans le supprimer.",
    )
    order = models.PositiveIntegerField(
        default=0,
        help_text="Ordre d'affichage (croissant).",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-published_at", "order"]
        verbose_name = "Post reseaux sociaux"
        verbose_name_plural = "Posts reseaux sociaux"

    def __str__(self):
        return f"[{self.get_platform_display()}] {self.excerpt[:60]}"
