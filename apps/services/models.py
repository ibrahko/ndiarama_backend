from django.db import models


class Service(models.Model):
    CATEGORY_CONSULTING = "consulting"
    CATEGORY_PROGRAM = "program"
    CATEGORY_TRAINING = "training"

    CATEGORY_CHOICES = (
        (CATEGORY_CONSULTING, "Consulting"),
        (CATEGORY_PROGRAM, "Programme"),
        (CATEGORY_TRAINING, "Formation"),
    )

    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)

    short_description = models.CharField(max_length=500, blank=True)
    description = models.TextField(blank=True)

    icon = models.CharField(
        max_length=100,
        blank=True,
        help_text="Classe d’icône front (optionnel, ex: 'fi fi-consulting').",
    )

    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    is_highlighted = models.BooleanField(
        default=False,
        help_text="Mettre en avant sur la page d’accueil.",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["category", "order", "title"]

    def __str__(self):
        return self.title