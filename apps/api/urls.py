from django.urls import path

from apps.api.views import HomeView, HealthView

urlpatterns = [
    path("home/", HomeView.as_view(), name="api-home"),
    path("health/", HealthView.as_view(), name="api-health"),
]
