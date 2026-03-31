from rest_framework import serializers

from .models import ProgramHighlight, CommunityFeature


class ProgramHighlightSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProgramHighlight
        fields = [
            "id",
            "name",
            "slug",
            "short_description",
            "external_link",
            "order",
            "is_active",
        ]


class CommunityFeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommunityFeature
        fields = [
            "id",
            "title",
            "description",
            "telegram_link",
            "show_newsletter_button",
            "order",
            "is_active",
        ]