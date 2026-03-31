from django.db import models


class SiteSettings(models.Model):
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