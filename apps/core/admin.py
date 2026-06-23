"""
Admin Django — Application core.
"""
from dataclasses import dataclass
from django.contrib import admin
from django.utils.html import format_html
from unfold.admin import ModelAdmin
from unfold.decorators import display

from apps.accounts.permissions import RoleBasedAdminMixin
from .models import SiteSettings, TeamMember, Testimonial


@dataclass
class HeaderPhoto:
    """Objet image compatible avec le template display_header d'Unfold."""
    path: str
    width: int | None = 40
    height: int | None = 40
    squared: bool = False
    borderless: bool = False
    as_background: bool = False


def _initials(name: str) -> str:
    parts = name.split()
    return "".join(p[0].upper() for p in parts[:2]) if parts else "?"


@admin.register(SiteSettings)
class SiteSettingsAdmin(RoleBasedAdminMixin, ModelAdmin):
    compressed_fields = True

    fieldsets = (
        ("Identite du site", {
            "description": "Ces informations apparaissent dans le Hero de la page d'accueil.",
            "fields": ("site_name", "hero_slogan", "mission_text"),
        }),
        ("Video Hero", {
            "description": (
                "Collez ici l'URL directe de votre video (YouTube, Cloudflare Stream, S3). "
                "Laissez vide pour afficher l'animation waveform par defaut."
            ),
            "fields": ("hero_video_url",),
        }),
        ("Coordonnees", {
            "description": "Affichees sur la page Contact.",
            "fields": ("address", "email", "phone"),
        }),
        ("Reseaux sociaux", {
            "description": "URLs completes (ex: https://www.linkedin.com/company/ndiarama).",
            "fields": ("linkedin_url", "tiktok_url", "youtube_url"),
        }),
    )

    def has_add_permission(self, request):
        if SiteSettings.objects.exists():
            return False
        return super().has_add_permission(request)

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(TeamMember)
class TeamMemberAdmin(RoleBasedAdminMixin, ModelAdmin):
    compressed_fields = True
    list_display = ("display_member", "role", "order", "is_active_badge")
    list_display_links = ("display_member",)
    list_filter = ("is_active",)
    list_editable = ("order",)
    search_fields = ("name", "role")
    ordering = ("order", "name")

    fieldsets = (
        ("Informations du membre", {
            "fields": ("name", "role", "short_bio", "photo"),
        }),
        ("Affichage", {
            "description": "Ordre faible (1, 2, 3) = affiche en premier. Decochez 'Actif' pour masquer.",
            "fields": ("order", "is_active"),
        }),
    )

    @display(description="Membre", header=True)
    def display_member(self, obj):
        photo = HeaderPhoto(path=obj.photo.url) if obj.photo else None
        return [obj.name, obj.role, _initials(obj.name), photo]

    @display(description="Visible", boolean=True)
    def is_active_badge(self, obj):
        return obj.is_active


@admin.register(Testimonial)
class TestimonialAdmin(RoleBasedAdminMixin, ModelAdmin):
    compressed_fields = True
    list_display = ("display_testimonial", "position", "message_preview", "order", "is_active_badge")
    list_display_links = ("display_testimonial",)
    list_filter = ("is_active",)
    list_editable = ("order",)
    search_fields = ("name", "position", "message")
    ordering = ("order", "name")

    fieldsets = (
        ("Temoignage", {
            "description": "Message et photo apparaissent dans le carrousel de la page d'accueil.",
            "fields": ("name", "position", "message", "photo"),
        }),
        ("Affichage", {
            "fields": ("order", "is_active"),
        }),
    )

    @display(description="Personne", header=True)
    def display_testimonial(self, obj):
        photo = HeaderPhoto(path=obj.photo.url) if obj.photo else None
        return [obj.name, obj.position, _initials(obj.name), photo]

    @display(description="Message")
    def message_preview(self, obj):
        return obj.message[:80] + "..." if len(obj.message) > 80 else obj.message

    @display(description="Visible", boolean=True)
    def is_active_badge(self, obj):
        return obj.is_active
