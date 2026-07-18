"""
Vues DRF pour l'application communication.
Fournit les endpoints consommés par le frontend NDIARAMA.
"""
import logging

from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from rest_framework import generics, viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.views import APIView
from apps.accounts.api_permissions import IsAdminOnly

# Nom du champ honeypot : invisible pour les humains (masqué en CSS),
# rempli par les bots. Si présent et non vide → on ignore silencieusement.
HONEYPOT_FIELD = "website"


def _is_bot(request) -> bool:
    return bool(str(request.data.get(HONEYPOT_FIELD, "")).strip())

from .models import NewsletterSubscriber, ContactMessage
from .serializers import NewsletterSubscriberSerializer, ContactMessageSerializer
from .services import subscribe_to_mailchimp, create_and_send_campaign

logger = logging.getLogger(__name__)

class NewsletterSubscribeView(generics.CreateAPIView):
    queryset = NewsletterSubscriber.objects.all()
    serializer_class = NewsletterSubscriberSerializer
    permission_classes = [AllowAny]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "newsletter"

    def create(self, request, *args, **kwargs):
        # Honeypot : réponse "succès" factice, rien n'est enregistré.
        if _is_bot(request):
            logger.warning("Honeypot newsletter déclenché — requête ignorée.")
            return Response(
                {"success": True, "message": "Inscription réussie !"},
                status=status.HTTP_201_CREATED,
            )

        # Doublon : vérifié AVANT la validation du serializer, sinon le
        # validateur d'unicité renvoie un 400 générique et ce message
        # convivial n'est jamais atteint.
        email_raw = str(request.data.get("email", "")).lower().strip()
        if email_raw and NewsletterSubscriber.objects.filter(email=email_raw).exists():
            return Response(
                {"success": False, "message": "Cet email est déjà inscrit."},
                status=status.HTTP_200_OK
            )

        serializer = self.get_serializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                {"success": False, "errors": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )

        email = serializer.validated_data.get("email")
        whatsapp = serializer.validated_data.get("whatsapp", "")

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


class ContactMessageCreateView(generics.CreateAPIView):
    """
    POST /api/communication/contact/
    Sauvegarde le message en base ET envoie une notification email à l'équipe.
    """
    queryset = ContactMessage.objects.all()
    serializer_class = ContactMessageSerializer
    permission_classes = [AllowAny]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "contact"

    def create(self, request, *args, **kwargs):
        # Honeypot : réponse "succès" factice, rien n'est enregistré.
        if _is_bot(request):
            logger.warning("Honeypot contact déclenché — requête ignorée.")
            return Response(
                {"success": True, "message": "Message envoyé avec succès."},
                status=status.HTTP_201_CREATED,
            )

        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {"success": False, "errors": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

        msg = serializer.save()

        # ── Notification email à l'équipe ──
        self._notify_team(msg)

        return Response(
            {"success": True, "message": "Message envoyé avec succès."},
            status=status.HTTP_201_CREATED,
        )

    @staticmethod
    def _notify_team(msg: ContactMessage) -> None:
        """
        Envoie un email de notification à CONTACT_EMAIL (défini dans les settings).
        En cas d'erreur (mauvaise config SMTP), on log sans faire planter la requête.
        """
        contact_email = getattr(settings, "CONTACT_EMAIL", None)
        if not contact_email:
            logger.warning("CONTACT_EMAIL non défini — notification email ignorée.")
            return

        subject = f"[NDIARAMA] Nouveau message : {msg.subject or 'Sans sujet'}"

        text_body = (
            f"Nouveau message reçu via le formulaire de contact NDIARAMA.\n\n"
            f"De      : {msg.name} <{msg.email}>\n"
            f"Sujet   : {msg.subject or '(non précisé)'}\n"
            f"Reçu le : {msg.created_at.strftime('%d/%m/%Y à %H:%M')}\n\n"
            f"--- Message ---\n{msg.message}\n\n"
            f"---\n"
            f"Répondre directement à : {msg.email}\n"
            f"Voir dans l'admin Django : /admin/communication/contactmessage/{msg.pk}/change/"
        )

        html_body = f"""
        <div style="font-family:Inter,Arial,sans-serif;max-width:600px;margin:auto;padding:24px;background:#f8f4ef;">
          <div style="background:#2b211d;padding:16px 24px;border-radius:8px 8px 0 0;">
            <h1 style="color:#e9c1a4;font-size:18px;margin:0;">NDIARAMA — Nouveau message</h1>
          </div>
          <div style="background:#fff;padding:24px;border-radius:0 0 8px 8px;border:1px solid #e3d4c8;">
            <table style="width:100%;border-collapse:collapse;margin-bottom:20px;">
              <tr>
                <td style="padding:8px 0;color:#888;font-size:13px;width:80px;">De</td>
                <td style="padding:8px 0;font-weight:600;color:#2b211d;">{msg.name} &lt;{msg.email}&gt;</td>
              </tr>
              <tr>
                <td style="padding:8px 0;color:#888;font-size:13px;">Sujet</td>
                <td style="padding:8px 0;color:#2b211d;">{msg.subject or '(non précisé)'}</td>
              </tr>
              <tr>
                <td style="padding:8px 0;color:#888;font-size:13px;">Reçu le</td>
                <td style="padding:8px 0;color:#2b211d;">{msg.created_at.strftime('%d/%m/%Y à %H:%M')}</td>
              </tr>
            </table>
            <div style="background:#f8f4ef;padding:16px;border-radius:8px;border-left:3px solid #cc8a5f;">
              <p style="margin:0;font-size:14px;color:#444;line-height:1.6;white-space:pre-wrap;">{msg.message}</p>
            </div>
            <div style="margin-top:24px;padding-top:16px;border-top:1px solid #e3d4c8;">
              <a href="mailto:{msg.email}?subject=Re: {msg.subject or 'Votre message'}"
                 style="display:inline-block;background:#cc8a5f;color:#fff;padding:10px 20px;border-radius:8px;text-decoration:none;font-size:13px;font-weight:600;">
                Répondre à {msg.name}
              </a>
            </div>
          </div>
          <p style="text-align:center;font-size:11px;color:#aaa;margin-top:16px;">
            NDIARAMA Media &amp; Consulting — notification automatique
          </p>
        </div>
        """

        try:
            send_mail(
                subject=subject,
                message=text_body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[contact_email],
                html_message=html_body,
                fail_silently=False,
            )
            logger.info("Notification email envoyée pour le message #%s", msg.pk)
        except Exception as exc:
            # On ne fait pas planter la requête si l'email échoue
            logger.error("Échec envoi notification email message #%s : %s", msg.pk, exc)


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
