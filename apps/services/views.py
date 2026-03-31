from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from apps.accounts.api_permissions import IsAdminOrReadOnly
from .models import Service
from .serializers import ServiceSerializer


class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.filter(is_active=True)
    serializer_class = ServiceSerializer

    def get_permissions(self):
        if self.request.method in ("GET", "HEAD", "OPTIONS"):
            return [AllowAny()]
        return [IsAdminOrReadOnly()]