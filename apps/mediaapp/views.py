from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from apps.accounts.api_permissions import IsAdminOrReadOnly
from .models import Show, Episode
from .serializers import ShowSerializer, EpisodeSerializer


class ShowViewSet(viewsets.ModelViewSet):
    queryset = Show.objects.all()
    serializer_class = ShowSerializer

    def get_permissions(self):
        if self.request.method in ("GET", "HEAD", "OPTIONS"):
            return [AllowAny()]
        return [IsAdminOrReadOnly()]


class EpisodeViewSet(viewsets.ModelViewSet):
    queryset = Episode.objects.select_related("show").all()
    serializer_class = EpisodeSerializer

    def get_permissions(self):
        if self.request.method in ("GET", "HEAD", "OPTIONS"):
            return [AllowAny()]
        return [IsAdminOrReadOnly()]

    def get_queryset(self):
        qs = super().get_queryset().filter(show__is_active=True, is_published=True)
        show_slug = self.request.query_params.get("show")
        if show_slug:
            qs = qs.filter(show__slug=show_slug)
        return qs