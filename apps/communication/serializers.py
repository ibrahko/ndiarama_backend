from rest_framework import serializers

from .models import NewsletterSubscriber, ContactMessage


class NewsletterSubscriberSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsletterSubscriber
        fields = [
            "id",
            "email",
            "first_name",
            "source",
            "created_at",
        ]
        read_only_fields = ["id", "created_at"]


class ContactMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMessage
        fields = [
            "id",
            "name",
            "email",
            "subject",
            "message",
            "created_at",
            "handled",
        ]
        read_only_fields = ["id", "created_at", "handled"]