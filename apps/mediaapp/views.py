"""
Vues DRF pour l'application mediaapp.
Fournit les endpoints consommés par le frontend NDIARAMA.

Lecture seule : le contenu est géré exclusivement via l'admin Django.
(Éviter d'exposer des écritures Basic/Session auth sur l'API publique.)
"""
from django.db.models import Prefetch
from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from .models import Show, Episode
from .serializers import ShowSerializer, EpisodeSerializer


class ShowViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Lecture publique des émissions actives, détail par slug.
    Les épisodes imbriqués sont limités aux épisodes publiés
    (Prefetch → une seule requête, pas de N+1).
    """
    queryset = Show.objects.filter(is_active=True).prefetch_related(
        Prefetch(
            "episodes",
            queryset=Episode.objects.filter(is_published=True),
        )
    )
    serializer_class = ShowSerializer
    permission_classes = [AllowAny]
    lookup_field = "slug"


class EpisodeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Episode.objects.select_related("show").all()
    serializer_class = EpisodeSerializer
    permission_classes = [AllowAny]
    lookup_field = "slug"

    def get_queryset(self):
        qs = super().get_queryset().filter(show__is_active=True, is_published=True)
        show_slug = self.request.query_params.get("show")
        if show_slug:
            qs = qs.filter(show__slug=show_slug)
        return qs
