"""
Vues DRF pour l'application services.
Fournit les endpoints consommés par le frontend NDIARAMA.

Lecture seule : le contenu est géré exclusivement via l'admin Django.
"""
from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from .models import Service
from .serializers import ServiceSerializer


class ServiceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Service.objects.filter(is_active=True)
    serializer_class = ServiceSerializer
    permission_classes = [AllowAny]
    lookup_field = "slug"
