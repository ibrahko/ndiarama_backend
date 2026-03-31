from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import SiteSettingsView, TeamMemberViewSet, TestimonialViewSet

router = DefaultRouter()
router.register("team", TeamMemberViewSet, basename="team")
router.register("testimonials", TestimonialViewSet, basename="testimonials")

urlpatterns = [
    path("settings/", SiteSettingsView.as_view(), name="site-settings"),
]

urlpatterns += router.urls