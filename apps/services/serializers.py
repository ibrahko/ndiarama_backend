"""
Sérialiseurs DRF pour l'application services.
Exposent les modèles via l'API REST au frontend React.
"""
from rest_framework import serializers

from .models import Service


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = [
            "id",
            "category",
            "title",
            "slug",
            "short_description",
            "description",
            "icon",
            "order",
            "is_active",
            "is_highlighted",
        ]