from django.db import models


class Show(models.Model):
    """Émission / Podcast : ENGLISH CORNER, DEL PODCAST, etc."""

    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    tagline = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to="shows/", blank=True, null=True)

    # ✅ Liens plateformes du show
    youtube_channel_url = models.URLField(
        blank=True,
        help_text="Lien vers la chaîne YouTube ex: https://youtube.com/@ndiarama"
    )
    spotify_show_url = models.URLField(
        blank=True,
        help_text="Lien vers le show Spotify"
    )
    apple_podcast_url = models.URLField(
        blank=True,
        help_text="Lien vers Apple Podcasts"
    )

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
        ("both", "Vidéo + Audio"),  # ✅ ajout
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

    # ✅ URL principale (Spotify ou fichier audio)
    media_url = models.URLField(
        blank=True,
        help_text="Lien Spotify ou fichier audio hébergé."
    )

    # ✅ YouTube
    youtube_url = models.URLField(
        blank=True,
        help_text="URL complète YouTube ex: https://www.youtube.com/watch?v=abc123"
    )

    # ✅ Autres plateformes
    spotify_url = models.URLField(
        blank=True,
        help_text="Lien direct vers l'épisode Spotify"
    )
    apple_podcast_url = models.URLField(
        blank=True,
        help_text="Lien direct vers l'épisode Apple Podcasts"
    )

    # ✅ Miniature
    thumbnail = models.ImageField(
        upload_to="episodes/thumbnails/",
        blank=True,
        null=True,
        help_text="Miniature de l'épisode (optionnel, sinon auto depuis YouTube)"
    )

    duration = models.CharField(
        max_length=20,
        blank=True,
        help_text="Durée lisible ex: '12:30' ou '25 min'.",
    )

    published_at = models.DateTimeField()
    is_published = models.BooleanField(default=True)
    is_featured = models.BooleanField(
        default=False,
        help_text="À mettre en avant sur la page d'accueil.",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-published_at"]

    def __str__(self):
        return f"{self.show.title} - {self.title}"

    # ✅ Propriété pour extraire l'ID YouTube automatiquement
    @property
    def youtube_video_id(self) -> str | None:
        """
        Extrait l'ID YouTube depuis l'URL.
        https://www.youtube.com/watch?v=abc123  →  abc123
        https://youtu.be/abc123                 →  abc123
        """
        if not self.youtube_url:
            return None

        import re
        patterns = [
            r"youtube\.com/watch\?v=([a-zA-Z0-9_-]{11})",
            r"youtu\.be/([a-zA-Z0-9_-]{11})",
            r"youtube\.com/embed/([a-zA-Z0-9_-]{11})",
        ]
        for pattern in patterns:
            match = re.search(pattern, self.youtube_url)
            if match:
                return match.group(1)
        return None

    @property
    def youtube_embed_url(self) -> str | None:
        """Retourne l'URL d'embed prête à utiliser dans un iframe."""
        video_id = self.youtube_video_id
        if video_id:
            return f"https://www.youtube.com/embed/{video_id}"
        return None

    @property
    def has_video(self) -> bool:
        return bool(self.youtube_url)

    @property
    def has_audio(self) -> bool:
        return bool(self.media_url or self.spotify_url)