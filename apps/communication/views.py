from rest_framework import generics, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated

from apps.accounts.api_permissions import IsAdminOnly
from .models import NewsletterSubscriber, ContactMessage
from .serializers import NewsletterSubscriberSerializer, ContactMessageSerializer


class NewsletterSubscribeView(generics.CreateAPIView):
    queryset = NewsletterSubscriber.objects.all()
    serializer_class = NewsletterSubscriberSerializer
    permission_classes = [AllowAny]


class ContactMessageCreateView(generics.CreateAPIView):
    queryset = ContactMessage.objects.all()
    serializer_class = ContactMessageSerializer
    permission_classes = [AllowAny]


class NewsletterSubscriberAdminViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = NewsletterSubscriber.objects.all()
    serializer_class = NewsletterSubscriberSerializer
    permission_classes = [IsAdminOnly]


class ContactMessageAdminViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ContactMessage.objects.all()
    serializer_class = ContactMessageSerializer
    permission_classes = [IsAdminOnly]