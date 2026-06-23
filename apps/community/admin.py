"""
Admin Django — Application community.
"""
from django.contrib import admin
from django.utils.html import format_html
from unfold.admin import ModelAdmin
from unfold.decorators import display

from apps.accounts.permissions import RoleBasedAdminMixin
from .models import ProgramHighlight, CommunityFeature, SocialPost


@admin.register(ProgramHighlight)
class ProgramHighlightAdmin(RoleBasedAdminMixin, ModelAdmin):
    compressed_fields = True
    list_display = ("name", "short_desc", "external_link_badge", "order", "is_active_badge")
    list_display_links = ("name",)
    list_filter = ("is_active",)
    list_editable = ("order",)
    search_fields = ("name", "short_description")
    prepopulated_fields = {"slug": ("name",)}
    ordering = ("order", "name")

    fieldsets = (
        ("Programme", {
            "description": "Ces programmes apparaissent dans la section Communaute du site (Chevening, YALI, Fulbright...).",
            "fields": ("name", "slug", "short_description", "external_link"),
        }),
        ("Affichage", {
            "fields": ("order", "is_active"),
        }),
    )

    @display(description="Description")
    def short_desc(self, obj):
        return obj.short_description[:60] + "..." if len(obj.short_description) > 60 else obj.short_description

    @display(description="Lien externe")
    def external_link_badge(self, obj):
        if obj.external_link:
            return format_html(
                '<a href="{}" target="_blank" style="color:#cc8a5f;text-decoration:none;">Voir</a>',
                obj.external_link,
            )
        return "—"

    @display(description="Actif", boolean=True)
    def is_active_badge(self, obj):
        return obj.is_active


@admin.register(CommunityFeature)
class CommunityFeatureAdmin(RoleBasedAdminMixin, ModelAdmin):
    compressed_fields = True
    list_display = ("title", "telegram_badge", "newsletter_badge", "order", "is_active_badge")
    list_display_links = ("title",)
    list_filter = ("is_active", "show_newsletter_button")
    list_editable = ("order",)
    search_fields = ("title", "description")
    ordering = ("order", "title")

    fieldsets = (
        ("Avantage communaute", {
            "description": "Fiches descriptives affichees sur la page Communaute.",
            "fields": ("title", "description"),
        }),
        ("Liens et actions", {
            "description": (
                "Lien Telegram : bouton 'Rejoindre' vers le groupe prive. "
                "Bouton newsletter : affiche un bouton 'S'inscrire' sur cette fiche."
            ),
            "fields": ("telegram_link", "show_newsletter_button"),
        }),
        ("Affichage", {
            "fields": ("order", "is_active"),
        }),
    )

    @display(description="Telegram")
    def telegram_badge(self, obj):
        if obj.telegram_link:
            return format_html('<span style="color:#2e7d32;font-weight:600;">Configure</span>')
        return format_html('<span style="color:#999;">—</span>')

    @display(description="Newsletter", boolean=True)
    def newsletter_badge(self, obj):
        return obj.show_newsletter_button

    @display(description="Actif", boolean=True)
    def is_active_badge(self, obj):
        return obj.is_active


@admin.register(SocialPost)
class SocialPostAdmin(ModelAdmin):
    compressed_fields = True
    list_display = (
        "platform_badge", "excerpt_preview",
        "published_at", "likes", "order", "is_active",
    )
    list_display_links = ("excerpt_preview",)
    list_filter = ("platform", "is_active")
    list_editable = ("order", "is_active")
    search_fields = ("excerpt", "url")
    ordering = ("-published_at", "order")
    date_hierarchy = "published_at"

    fieldsets = (
        ("Post reseaux sociaux", {
            "description": (
                "Ces posts s'affichent dans la section 'Derniers posts' de la page Communaute. "
                "Mettez a jour manuellement quand vous publiez un nouveau post marquant."
            ),
            "fields": ("platform", "excerpt", "url", "published_at", "likes"),
        }),
        ("Affichage", {
            "fields": ("order", "is_active"),
        }),
    )

    @display(description="Reseau")
    def platform_badge(self, obj):
        config = {
            "linkedin": ("#0077b5", "LinkedIn"),
            "tiktok":   ("#000000", "TikTok"),
        }
        color, label = config.get(obj.platform, ("#555", obj.platform))
        return format_html(
            '<span style="background:{};color:#fff;padding:2px 8px;'
            'border-radius:12px;font-size:11px;">{}</span>',
            color, label,
        )

    @display(description="Extrait")
    def excerpt_preview(self, obj):
        return obj.excerpt[:80] + "..." if len(obj.excerpt) > 80 else obj.excerpt
