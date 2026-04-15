from rest_framework import generics, viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from apps.accounts.api_permissions import IsAdminOnly

from .models import NewsletterSubscriber, ContactMessage
from .serializers import NewsletterSubscriberSerializer, ContactMessageSerializer
from .services import subscribe_to_mailchimp
from .services import create_and_send_campaign


class NewsletterSubscribeView(generics.CreateAPIView):
    queryset = NewsletterSubscriber.objects.all()
    serializer_class = NewsletterSubscriberSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                {"success": False, "errors": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )

        email = serializer.validated_data.get("email")
        whatsapp = serializer.validated_data.get("whatsapp", "")

        # Vérifier doublon
        if NewsletterSubscriber.objects.filter(email=email).exists():
            return Response(
                {"success": False, "message": "Cet email est déjà inscrit."},
                status=status.HTTP_200_OK
            )

        # Sauvegarder en base
        subscriber = serializer.save()

        # ✅ Envoyer à Mailchimp
        mailchimp_result = subscribe_to_mailchimp(email, whatsapp)

        if mailchimp_result.get("success"):
            subscriber.mailchimp_synced = True
            subscriber.save(update_fields=["mailchimp_synced"])

        return Response(
            {
                "success": True,
                "message": "Inscription réussie ! Bienvenue dans la communauté NDIARAMA.",
                "mailchimp_synced": mailchimp_result.get("success", False),
            },
            status=status.HTTP_201_CREATED
        )


# --- Vues admin inchangées ---
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


class SendNewsletterCampaignView(APIView):
    """
    Réservé aux admins.
    POST /api/communication/send-campaign/
    Body: { "subject": "...", "html_content": "...", "preview_text": "..." }
    """
    permission_classes = [IsAdminOnly]

    def post(self, request):
        subject = request.data.get("subject", "").strip()
        html_content = request.data.get("html_content", "").strip()
        preview_text = request.data.get("preview_text", "")

        if not subject or not html_content:
            return Response(
                {"success": False, "error": "subject et html_content sont requis."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        result = create_and_send_campaign(subject, html_content, preview_text)

        if result["success"]:
            return Response(result, status=status.HTTP_200_OK)
        else:
            return Response(result, status=status.HTTP_502_BAD_GATEWAY)
