from rest_framework import serializers

from .models import SiteSettings, TeamMember, Testimonial


class SiteSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteSettings
        fields = [
            "site_name",
            "hero_slogan",
            "hero_video_url",
            "mission_text",
            "address",
            "email",
            "phone",
            "linkedin_url",
            "tiktok_url",
            "youtube_url",
        ]


class TeamMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamMember
        fields = [
            "id",
            "name",
            "role",
            "short_bio",
            "photo",
            "order",
        ]


class TestimonialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Testimonial
        fields = [
            "id",
            "name",
            "position",
            "message",
            "photo",
            "order",
        ]