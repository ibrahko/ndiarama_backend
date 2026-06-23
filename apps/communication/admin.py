"""
Admin Django — Application communication.
"""
from django.contrib import admin
from django.shortcuts import render
from django.urls import path, reverse
from django.contrib import messages
from django.utils.html import format_html
from unfold.admin import ModelAdmin
from unfold.decorators import display

from .models import NewsletterSubscriber, ContactMessage
from .services import create_and_send_campaign


@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(ModelAdmin):
    compressed_fields = True
    list_display = (
        "email", "whatsapp", "source_badge",
        "mailchimp_badge", "created_at",
    )
    list_filter = ("source", "mailchimp_synced")
    search_fields = ("email", "whatsapp")
    readonly_fields = ("email", "whatsapp", "source", "mailchimp_synced", "created_at")
    ordering = ("-created_at",)

    fieldsets = (
        ("Abonne", {
            "description": "Les abonnes sont ajoutes automatiquement via les formulaires du site.",
            "fields": ("email", "whatsapp", "source", "mailchimp_synced", "created_at"),
        }),
    )

    def has_add_permission(self, request):
        return False

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "send-campaign/",
                self.admin_site.admin_view(self.send_campaign_view),
                name="communication_send_campaign",
            ),
        ]
        return custom_urls + urls

    def send_campaign_view(self, request):
        context = {
            **self.admin_site.each_context(request),
            "title": "Envoyer une Newsletter",
            "opts": self.model._meta,
            "form_data": {},
        }
        if request.method == "POST":
            subject = request.POST.get("subject", "").strip()
            preview_text = request.POST.get("preview_text", "").strip()
            html_content = request.POST.get("html_content", "").strip()
            test_email = request.POST.get("test_email", "").strip()
            action = request.POST.get("action")
            context["form_data"] = request.POST

            if not subject or not html_content:
                messages.error(request, "L'objet et le contenu sont obligatoires.")
                return render(request, "admin/communication/send_campaign.html", context)

            result = create_and_send_campaign(
                subject, html_content, preview_text,
                test_email=test_email if action == "test" else None,
            )
            if result["success"]:
                messages.success(request, f"Envoye — ID : {result.get('campaign_id')}")
            else:
                messages.error(request, f"Erreur ({result.get('step', '?')}) : {result.get('error')}")

        return render(request, "admin/communication/send_campaign.html", context)

    @display(description="Origine")
    def source_badge(self, obj):
        if obj.source:
            return format_html(
                '<span style="background:#f3f4f6;color:#555;padding:2px 8px;'
                'border-radius:8px;font-size:11px;">{}</span>',
                obj.source,
            )
        return "—"

    @display(description="Mailchimp", boolean=True)
    def mailchimp_badge(self, obj):
        return obj.mailchimp_synced


@admin.register(ContactMessage)
class ContactMessageAdmin(ModelAdmin):
    compressed_fields = True
    list_display = (
        "handled_badge", "name", "email_link",
        "subject", "created_at",
    )
    list_display_links = ("name",)
    list_filter = ("handled",)
    search_fields = ("name", "email", "subject", "message")
    readonly_fields = ("name", "email", "subject", "message", "created_at")
    ordering = ("-created_at",)

    fieldsets = (
        ("Message recu", {
            "description": (
                "Message envoye via le formulaire de contact du site. "
                "Cochez 'Traite' une fois que vous avez repondu."
            ),
            "fields": ("name", "email", "subject", "message", "created_at", "handled"),
        }),
    )

    def has_add_permission(self, request):
        return False

    @display(description="Statut")
    def handled_badge(self, obj):
        if obj.handled:
            return format_html(
                '<span style="background:#2e7d32;color:#fff;padding:2px 8px;'
                'border-radius:12px;font-size:11px;">Traite</span>'
            )
        return format_html(
            '<span style="background:#e65100;color:#fff;padding:2px 8px;'
            'border-radius:12px;font-size:11px;">Nouveau</span>'
        )

    @display(description="Email")
    def email_link(self, obj):
        return format_html(
            '<a href="mailto:{}?subject=Re: {}" style="color:#cc8a5f;">{}</a>',
            obj.email,
            obj.subject or "Votre message",
            obj.email,
        )
