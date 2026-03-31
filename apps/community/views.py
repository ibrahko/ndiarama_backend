from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from apps.accounts.api_permissions import IsAdminOrReadOnly
from .models import ProgramHighlight, CommunityFeature
from .serializers import ProgramHighlightSerializer, CommunityFeatureSerializer


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