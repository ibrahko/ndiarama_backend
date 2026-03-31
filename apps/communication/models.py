from django.db import models


class NewsletterSubscriber(models.Model):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=150, blank=True)
    source = models.CharField(
        max_length=100,
        blank=True,
        help_text="Origine de l’inscription (footer, community, autre).",
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.email


class ContactMessage(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    subject = models.CharField(max_length=255, blank=True)
    message = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    handled = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} - {self.subject or 'Message'}"