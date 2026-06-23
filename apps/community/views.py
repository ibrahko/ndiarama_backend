"""
Vues DRF pour l'application community.
"""
from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from apps.accounts.api_permissions import IsAdminOrReadOnly
from .models import ProgramHighlight, CommunityFeature, SocialPost
from .serializers import ProgramHighlightSerializer, CommunityFeatureSerializer, SocialPostSerializer


class ProgramHighlightViewSet(viewsets.ModelViewSet):
    queryset = ProgramHighlight.objects.filter(is_active=True)
    serializer_class = ProgramHighlightSerializer

    def get_permissions(self):
        if self.request.method in ("GET", "HEAD", "OPTIONS"):
            return [AllowAny()]
        return [IsAdminOrReadOnly()]


class CommunityFeatureViewSet(viewsets.ModelViewSet):
    queryset = CommunityFeature.objects.filter(is_active=True)
    serializer_class = CommunityFeatureSerializer

    def get_permissions(self):
        if self.request.method in ("GET", "HEAD", "OPTIONS"):
            return [AllowAny()]
        return [IsAdminOrReadOnly()]


class SocialPostViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Endpoint lecture seule pour les posts reseaux sociaux.
    GET /api/community/social-posts/
    """
    queryset = SocialPost.objects.filter(is_active=True)
    serializer_class = SocialPostSerializer
    permission_classes = [AllowAny]
