from rest_framework.routers import DefaultRouter

from .views import ProgramHighlightViewSet, CommunityFeatureViewSet

router = DefaultRouter()
router.register("programs", ProgramHighlightViewSet, basename="programs")
router.register("features", CommunityFeatureViewSet, basename="community-features")

urlpatterns = router.urls