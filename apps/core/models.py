from django.db import models


class SiteSettings(models.Model):
    """
    Réglages globaux du site — singleton.
    L'admin empêche déjà l'ajout d'une 2e instance ; save() garantit
    la même règle au niveau du modèle (API, shell, scripts).
    """
    site_name = models.CharField(
        max_length=255,
        default="NDIARAMA Media & Consulting",
    )
    hero_slogan = models.CharField(max_length=255, blank=True)
    hero_video_url = models.URLField(blank=True)
    mission_text = models.TextField(blank=True)

    address = models.CharField(max_length=255, blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=50, blank=True)

    linkedin_url = models.URLField(blank=True)
    tiktok_url = models.URLField(blank=True)
    youtube_url = models.URLField(blank=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Site settings"

    def save(self, *args, **kwargs):
        # Force une instance unique : toute sauvegarde écrase pk=1.
        self.pk = 1
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # Le singleton ne se supprime pas (cohérent avec l'admin).
        raise models.ProtectedError(
            "SiteSettings est un singleton et ne peut pas être supprimé.", [self]
        )

    @classmethod
    def load(cls) -> "SiteSettings":
        """Renvoie l'instance unique, créée à la volée si nécessaire."""
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj

    def __str__(self):
        return "Site settings"


class TeamMember(models.Model):
    name = models.CharField(max_length=255)
    role = models.CharField(max_length=255)
    short_bio = models.CharField(max_length=500, blank=True)
    photo = models.ImageField(upload_to="team/", blank=True, null=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["order", "name"]

    def __str__(self):
        return self.name


class Testimonial(models.Model):
    name = models.CharField(max_length=255)
    position = models.CharField(max_length=255, blank=True)
    message = models.TextField()
    photo = models.ImageField(upload_to="testimonials/", blank=True, null=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["order", "name"]

    def __str__(self):
        return self.name