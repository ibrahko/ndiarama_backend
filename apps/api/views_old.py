from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.db import connections
from django.db.utils import OperationalError
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
from .serializers.home import (
    SiteSettingsSerializer,
    TeamMemberSerializer,
    TestimonialSerializer,
    ShowHomeSerializer,
    EpisodeFeaturedSerializer,
    ServiceHighlightSerializer,
)


class HomeView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        # Site settings (unique)
        settings_obj = SiteSettings.objects.first()
        settings_data = (
            SiteSettingsSerializer(settings_obj).data if settings_obj else None
        )

        # Équipe active
        team = TeamMember.objects.filter(is_active=True)
        team_data = TeamMemberSerializer(team, many=True).data

        # Témoignages actifs
        testimonials = Testimonial.objects.filter(is_active=True)
        testimonials_data = TestimonialSerializer(testimonials, many=True).data

        # Shows actifs avec quelques épisodes chacun
        shows = Show.objects.filter(is_active=True).order_by("order", "title")
        shows_data = ShowSerializer(shows, many=True).data

        # Episodes mis en avant (is_featured)
        featured_episodes = (
            Episode.objects.filter(
                is_published=True,
                is_featured=True,
                show__is_active=True,
            )
            .select_related("show")
            .order_by("-published_at")[:8]
        )
        featured_episodes_data = EpisodeSerializer(
            featured_episodes, many=True
        ).data

        # Services mis en avant
        highlighted_services = Service.objects.filter(
            is_active=True, is_highlighted=True
        ).order_by("order", "title")
        highlighted_services_data = ServiceSerializer(
            highlighted_services, many=True
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


class HealthView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        db_ok = True
        try:
            connections["default"].cursor()
        except OperationalError:
            db_ok = False

        data = {
            "status": "ok" if db_ok else "degraded",
            "database": db_ok,
        }
        status_code = 200 if db_ok else 503
        return Response(data, status=status_code)