# apps/communication/admin.py

from django.contrib import admin
from django.shortcuts import render
from django.urls import path, reverse
from django.contrib import messages
from django.utils.html import format_html

from .models import NewsletterSubscriber, ContactMessage
from .services import create_and_send_campaign


@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin):
    list_display = ["email", "whatsapp", "source", "mailchimp_synced", "created_at"]
    list_filter = ["source", "mailchimp_synced"]
    search_fields = ["email", "whatsapp"]
    readonly_fields = ["created_at", "mailchimp_synced"]

    # ✅ Bouton visible dans la liste
    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context["send_campaign_url"] = reverse(
            "admin:communication_send_campaign"
        )
        return super().changelist_view(request, extra_context=extra_context)

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
                return render(
                    request,
                    "admin/communication/send_campaign.html",
                    context
                )

            result = create_and_send_campaign(
                subject, html_content, preview_text,
                test_email=test_email if action == "test" else None,
            )

            if result["success"]:
                messages.success(
                    request,
                    f"✅ {result.get('message')} — ID campagne : {result.get('campaign_id')}"
                )
            else:
                messages.error(
                    request,
                    f"❌ Erreur ({result.get('step', '?')}) : {result.get('error')}"
                )

        return render(
            request,
            "admin/communication/send_campaign.html",
            context
        )


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ["name", "email", "subject", "handled", "created_at"]
    list_filter = ["handled"]
    search_fields = ["name", "email", "subject"]
    readonly_fields = ["name", "email", "subject", "message", "created_at"]

    def has_add_permission(self, request):
        return False