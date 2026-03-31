from rest_framework.routers import DefaultRouter

from .views import ShowViewSet, EpisodeViewSet

router = DefaultRouter()
router.register("shows", ShowViewSet, basename="shows")
router.register("episodes", EpisodeViewSet, basename="episodes")

urlpatterns = router.urls