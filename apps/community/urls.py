from rest_framework.routers import DefaultRouter

from .views import ProgramHighlightViewSet, CommunityFeatureViewSet, SocialPostViewSet

router = DefaultRouter()
router.register("programs",     ProgramHighlightViewSet, basename="programs")
router.register("features",     CommunityFeatureViewSet, basename="community-features")
router.register("social-posts", SocialPostViewSet,       basename="social-posts")

urlpatterns = router.urls
