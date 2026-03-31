from rest_framework import serializers

from .models import Show, Episode


class EpisodeSerializer(serializers.ModelSerializer):
    show_slug = serializers.ReadOnlyField(source="show.slug")
    show_title = serializers.ReadOnlyField(source="show.title")

    class Meta:
        model = Episode
        fields = [
            "id",
            "show",
            "show_slug",
            "show_title",
            "title",
            "slug",
            "description",
            "media_type",
            "media_url",
            "duration",
            "published_at",
            "is_published",
            "is_featured",
        ]
        read_only_fields = ["is_published", "is_featured"]


class ShowSerializer(serializers.ModelSerializer):
    episodes = EpisodeSerializer(many=True, read_only=True)

    class Meta:
        model = Show
        fields = [
            "id",
            "title",
            "slug",
            "tagline",
            "description",
            "image",
            "order",
            "is_active",
            "episodes",
        ]