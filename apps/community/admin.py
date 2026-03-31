from django.contrib import admin
from .models import ProgramHighlight, CommunityFeature
from apps.accounts.permissions import RoleBasedAdminMixin


@admin.register(ProgramHighlight)
class ProgramHighlightAdmin(RoleBasedAdminMixin):
    list_display = ("name", "order", "is_active")
    list_filter = ("is_active",)
    search_fields = ("name", "short_description")
    prepopulated_fields = {"slug": ("name",)}
    ordering = ("order", "name")


@admin.register(CommunityFeature)
class CommunityFeatureAdmin(RoleBasedAdminMixin):
    list_display = ("title", "order", "is_active", "show_newsletter_button")
    list_filter = ("is_active", "show_newsletter_button")
    search_fields = ("title", "description")
    ordering = ("order", "title")