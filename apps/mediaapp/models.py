from django.db import models


class Show(models.Model):
    """Émission / Podcast : ENGLISH CORNER, DEL PODCAST, etc."""

    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    tagline = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to="shows/", blank=True, null=True)

    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["order", "title"]

    def __str__(self):
        return self.title


class Episode(models.Model):
    MEDIA_TYPE_CHOICES = (
        ("audio", "Audio"),
        ("video", "Video"),
    )

    show = models.ForeignKey(
        Show,
        related_name="episodes",
        on_delete=models.CASCADE,
    )
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)

    media_type = models.CharField(max_length=10, choices=MEDIA_TYPE_CHOICES)
    media_url = models.URLField(
        help_text="Lien vers YouTube, Spotify ou fichier hébergé."
    )
    duration = models.CharField(
        max_length=20,
        blank=True,
        help_text="Durée lisible, ex: '12:30' ou '25 min'.",
    )

    published_at = models.DateTimeField()
    is_published = models.BooleanField(default=True)
    is_featured = models.BooleanField(
        default=False,
        help_text="À mettre en avant sur la page d’accueil.",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-published_at"]

    def __str__(self):
        return f"{self.show.title} - {self.title}"