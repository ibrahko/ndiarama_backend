"""
Tests de l'application communication : newsletter + contact.
"""
from unittest.mock import patch

from django.core import mail
from django.core.cache import cache
from django.test import TestCase, override_settings

from .models import NewsletterSubscriber, ContactMessage

NEWSLETTER_URL = "/api/communication/newsletter/"
CONTACT_URL = "/api/communication/contact/"

VALID_CONTACT = {
    "name": "Awa Traoré",
    "email": "awa@example.com",
    "subject": "Partenariat",
    "message": "Bonjour, je souhaite discuter d'un partenariat média avec vous.",
}


class NewsletterSubscribeTests(TestCase):
    def setUp(self):
        # Réinitialise les compteurs de throttling entre les tests
        cache.clear()

    @patch("apps.communication.views.subscribe_to_mailchimp")
    def test_subscribe_creates_subscriber_and_syncs_mailchimp(self, mock_mc):
        mock_mc.return_value = {"success": True}

        response = self.client.post(
            NEWSLETTER_URL,
            {"email": "Test@Example.com", "whatsapp": "+22370000000"},
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 201)
        self.assertTrue(response.json()["success"])
        subscriber = NewsletterSubscriber.objects.get()
        # L'email est normalisé en minuscules par le serializer
        self.assertEqual(subscriber.email, "test@example.com")
        self.assertTrue(subscriber.mailchimp_synced)
        mock_mc.assert_called_once()

    @patch("apps.communication.views.subscribe_to_mailchimp")
    def test_subscribe_still_saved_if_mailchimp_fails(self, mock_mc):
        mock_mc.return_value = {"success": False, "error": "timeout"}

        response = self.client.post(
            NEWSLETTER_URL,
            {"email": "offline@example.com"},
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 201)
        subscriber = NewsletterSubscriber.objects.get()
        self.assertFalse(subscriber.mailchimp_synced)

    @patch("apps.communication.views.subscribe_to_mailchimp")
    def test_duplicate_email_returns_friendly_message(self, mock_mc):
        NewsletterSubscriber.objects.create(email="dup@example.com")

        response = self.client.post(
            NEWSLETTER_URL,
            {"email": "Dup@Example.com"},
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertFalse(body["success"])
        self.assertIn("déjà inscrit", body["message"])
        self.assertEqual(NewsletterSubscriber.objects.count(), 1)
        mock_mc.assert_not_called()

    def test_invalid_email_returns_400(self):
        response = self.client.post(
            NEWSLETTER_URL,
            {"email": "pas-un-email"},
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertFalse(response.json()["success"])
        self.assertEqual(NewsletterSubscriber.objects.count(), 0)

    @patch("apps.communication.views.subscribe_to_mailchimp")
    def test_honeypot_filled_ignores_submission(self, mock_mc):
        response = self.client.post(
            NEWSLETTER_URL,
            {"email": "bot@example.com", "website": "http://spam.example"},
            content_type="application/json",
        )

        # Réponse "succès" factice, mais rien n'est enregistré ni envoyé
        self.assertEqual(response.status_code, 201)
        self.assertEqual(NewsletterSubscriber.objects.count(), 0)
        mock_mc.assert_not_called()


@override_settings(
    EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend",
    CONTACT_EMAIL="equipe@ndiarama.com",
)
class ContactMessageTests(TestCase):
    def setUp(self):
        cache.clear()

    def test_contact_creates_message_and_notifies_team(self):
        response = self.client.post(
            CONTACT_URL, VALID_CONTACT, content_type="application/json"
        )

        self.assertEqual(response.status_code, 201)
        self.assertTrue(response.json()["success"])

        msg = ContactMessage.objects.get()
        self.assertEqual(msg.email, "awa@example.com")
        self.assertFalse(msg.handled)

        # Notification envoyée à l'équipe
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn("equipe@ndiarama.com", mail.outbox[0].to)
        self.assertIn("Partenariat", mail.outbox[0].subject)

    def test_missing_fields_return_400(self):
        response = self.client.post(
            CONTACT_URL,
            {"name": "", "email": "pas-valide", "message": ""},
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 400)
        body = response.json()
        self.assertFalse(body["success"])
        self.assertIn("email", body["errors"])
        self.assertEqual(ContactMessage.objects.count(), 0)

    def test_honeypot_filled_ignores_submission(self):
        payload = {**VALID_CONTACT, "website": "http://spam.example"}
        response = self.client.post(
            CONTACT_URL, payload, content_type="application/json"
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(ContactMessage.objects.count(), 0)
        self.assertEqual(len(mail.outbox), 0)
