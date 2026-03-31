from django.contrib import admin
from .models import Show, Episode
from apps.accounts.permissions import RoleBasedAdminMixin


class EpisodeInline(admin.TabularInline):
    model = Episode
    extra = 1
    fields = (
        "title",
        "slug",
        "media_type",
        "media_url",
        "duration",
        "published_at",
        "is_published",
        "is_featured",
    )


@admin.register(Show)
class ShowAdmin(RoleBasedAdminMixin):
    list_display = ("title", "order", "is_active", "created_at")
    list_filter = ("is_active",)
    search_fields = ("title", "description")
    prepopulated_fields = {"slug": ("title",)}
    ordering = ("order", "title")
    inlines = [EpisodeInline]


@admin.register(Episode)
class EpisodeAdmin(RoleBasedAdminMixin):
    list_display = (
        "title",
        "show",
        "media_type",
        "published_at",
        "is_published",
        "is_featured",
    )
    list_filter = ("media_type", "is_published", "is_featured", "show")
    search_fields = ("title", "description")
    prepopulated_fields = {"slug": ("title",)}
    date_hierarchy = "published_at"
    ordering = ("-published_at",)