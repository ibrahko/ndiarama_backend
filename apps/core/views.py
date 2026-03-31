from rest_framework import generics, viewsets
from rest_framework.permissions import AllowAny

from .models import SiteSettings, TeamMember, Testimonial
from .serializers import (
    SiteSettingsSerializer,
    TeamMemberSerializer,
    TestimonialSerializer,
)


class SiteSettingsView(generics.RetrieveAPIView):
    permission_classes = [AllowAny]
    serializer_class = SiteSettingsSerializer

    def get_object(self):
        return SiteSettings.objects.first()


class TeamMemberViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = TeamMember.objects.filter(is_active=True)
    serializer_class = TeamMemberSerializer
    permission_classes = [AllowAny]


class TestimonialViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Testimonial.objects.filter(is_active=True)
    serializer_class = TestimonialSerializer
    permission_classes = [AllowAny]