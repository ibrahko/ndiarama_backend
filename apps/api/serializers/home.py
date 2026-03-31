from rest_framework import serializers

from apps.core.models import SiteSettings, TeamMember, Testimonial
from apps.mediaapp.models import Show, Episode
from apps.services.models import Service


class SiteSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteSettings
        fields = [
            "site_name",
            "hero_slogan",
            "hero_video_url",
        ]


class TeamMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamMember
        fields = [
            "id",
            "name",
            "role",
        ]


class TestimonialSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()

    class Meta:
        model = Testimonial
        fields = [
            "id",
            "message",
            "author",
        ]

    def get_author(self, obj):
        if hasattr(obj, "author") and obj.author:
            return obj.author
        if hasattr(obj, "name") and obj.name:
            return obj.name
        return None


class EpisodeMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = Episode
        fields = [
            "id",
            "title",
        ]


class EpisodeFeaturedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Episode
        fields = [
            "id",
            "title",
            "description",
        ]


class ShowHomeSerializer(serializers.ModelSerializer):
    episodes = serializers.SerializerMethodField()

    class Meta:
        model = Show
        fields = [
            "id",
            "title",
            "tagline",
            "episodes",
        ]

    def get_episodes(self, obj):
        episodes_qs = obj.episodes.filter(is_published=True).order_by("-published_at")[:3]
        return EpisodeMiniSerializer(episodes_qs, many=True).data


class ServiceHighlightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = [
            "id",
            "title",
            "short_description",
        ]
