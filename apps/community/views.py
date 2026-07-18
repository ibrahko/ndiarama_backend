"""
Vues DRF pour l'application community.

Lecture seule : le contenu est géré exclusivement via l'admin Django.
"""
from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from .models import ProgramHighlight, CommunityFeature, SocialPost
from .serializers import (
    ProgramHighlightSerializer,
    CommunityFeatureSerializer,
    SocialPostSerializer,
)


class ProgramHighlightViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ProgramHighlight.objects.filter(is_active=True)
    serializer_class = ProgramHighlightSerializer
    permission_classes = [AllowAny]


class CommunityFeatureViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CommunityFeature.objects.filter(is_active=True)
    serializer_class = CommunityFeatureSerializer
    permission_classes = [AllowAny]


class SocialPostViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Endpoint lecture seule pour les posts reseaux sociaux.
    GET /api/community/social-posts/
    """
    queryset = SocialPost.objects.filter(is_active=True)
    serializer_class = SocialPostSerializer
    permission_classes = [AllowAny]
