from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import (
    NewsletterSubscribeView,
    ContactMessageCreateView,
    NewsletterSubscriberAdminViewSet,
    ContactMessageAdminViewSet,
    SendNewsletterCampaignView,
)

router = DefaultRouter()
router.register(
    "newsletter-subscribers",
    NewsletterSubscriberAdminViewSet,
    basename="newsletter-subscribers",
)
router.register(
    "contact-messages",
    ContactMessageAdminViewSet,
    basename="contact-messages",
)

urlpatterns = [
    path("newsletter/", NewsletterSubscribeView.as_view(), name="newsletter-subscribe"),
    path("contact/", ContactMessageCreateView.as_view(), name="contact-create"),
    path("send-campaign/", SendNewsletterCampaignView.as_view(), name="send-campaign"),
]

urlpatterns += router.urls