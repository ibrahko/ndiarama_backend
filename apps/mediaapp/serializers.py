from rest_framework import serializers
from .models import Show, Episode


class EpisodeSerializer(serializers.ModelSerializer):
    # Champs existants
    show_slug = serializers.ReadOnlyField(source="show.slug")
    show_title = serializers.ReadOnlyField(source="show.title")

    # ✅ Nouvelles propriétés du modèle
    youtube_video_id = serializers.ReadOnlyField()
    youtube_embed_url = serializers.ReadOnlyField()
    has_video = serializers.ReadOnlyField()
    has_audio = serializers.ReadOnlyField()

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
            # Audio
            "media_url",
            "spotify_url",
            "apple_podcast_url",
            # YouTube
            "youtube_url",
            "youtube_video_id",
            "youtube_embed_url",
            # Média
            "thumbnail",
            "duration",
            "has_video",
            "has_audio",
            # Meta
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
            # ✅ Plateformes
            "youtube_channel_url",
            "spotify_show_url",
            "apple_podcast_url",
            # Episodes
            "episodes",
        ]