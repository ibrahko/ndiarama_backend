# apps/api/views/home.py

from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.core.models import SiteSettings, TeamMember, Testimonial
from apps.mediaapp.models import Show, Episode
from apps.services.models import Service

from apps.core.serializers import (
    SiteSettingsSerializer,
    TeamMemberSerializer,
    TestimonialSerializer,
)
from apps.mediaapp.serializers import ShowSerializer, EpisodeSerializer
from apps.services.serializers import ServiceSerializer


class HomeView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        settings_obj = SiteSettings.objects.first()
        settings_data = (
            SiteSettingsSerializer(settings_obj).data if settings_obj else None
        )

        team_qs = TeamMember.objects.filter(is_active=True).order_by("order", "name")
        team_data = TeamMemberSerializer(team_qs, many=True).data

        testimonials_qs = Testimonial.objects.filter(is_active=True).order_by(
            "order", "name"
        )
        testimonials_data = TestimonialSerializer(testimonials_qs, many=True).data

        shows_qs = (
            Show.objects.filter(is_active=True)
            .prefetch_related("episodes")
            .order_by("order", "title")
        )
        shows_data = ShowSerializer(shows_qs, many=True).data

        featured_episodes_qs = (
            Episode.objects.filter(
                is_published=True,
                is_featured=True,
                show__is_active=True,
            )
            .select_related("show")
            .order_by("-published_at")[:8]
        )
        featured_episodes_data = EpisodeSerializer(
            featured_episodes_qs, many=True
        ).data

        highlighted_services_qs = (
            Service.objects.filter(is_active=True, is_highlighted=True)
            .order_by("order", "title")
        )
        highlighted_services_data = ServiceSerializer(
            highlighted_services_qs, many=True
        ).data

        payload = {
            "settings": settings_data,
            "team": team_data,
            "testimonials": testimonials_data,
            "shows": shows_data,
            "featured_episodes": featured_episodes_data,
            "highlighted_services": highlighted_services_data,
        }

        return Response(payload)
