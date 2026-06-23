"""
Admin Django — Application services.
"""
from django.contrib import admin
from django.utils.html import format_html
from unfold.admin import ModelAdmin
from unfold.decorators import display

from apps.accounts.permissions import RoleBasedAdminMixin
from .models import Service

CATEGORY_COLORS = {
    "consulting": "#cc8a5f",
    "program":    "#2e7d32",
    "formation":  "#1565c0",
}
CATEGORY_LABELS = {
    "consulting": "Consulting",
    "program":    "Programme",
    "formation":  "Formation",
}


@admin.register(Service)
class ServiceAdmin(RoleBasedAdminMixin, ModelAdmin):
    compressed_fields = True
    list_display = (
        "title", "category_badge", "order",
        "is_highlighted_badge", "is_active_badge", "created_at",
    )
    list_display_links = ("title",)
    list_filter = ("category", "is_active", "is_highlighted")
    search_fields = ("title", "short_description", "description")
    prepopulated_fields = {"slug": ("title",)}
    ordering = ("category", "order", "title")

    fieldsets = (
        ("Informations du service", {
            "description": "Le titre et la description courte apparaissent dans les listes.",
            "fields": ("title", "slug", "category", "short_description", "description", "icon"),
        }),
        ("Affichage", {
            "description": (
                "Ordre : nombre faible = affiche en premier dans sa categorie. "
                "A la une : mis en avant sur la page d'accueil. "
                "Actif : decochez pour masquer sans supprimer."
            ),
            "fields": ("order", "is_highlighted", "is_active"),
        }),
    )

    @display(description="Categorie")
    def category_badge(self, obj):
        color = CATEGORY_COLORS.get(obj.category, "#555")
        label = CATEGORY_LABELS.get(obj.category, obj.get_category_display())
        return format_html(
            '<span style="background:{};color:#fff;padding:3px 10px;'
            'border-radius:12px;font-size:11px;">{}</span>',
            color, label,
        )

    @display(description="A la une", boolean=True)
    def is_highlighted_badge(self, obj):
        return obj.is_highlighted

    @display(description="Actif", boolean=True)
    def is_active_badge(self, obj):
        return obj.is_active
