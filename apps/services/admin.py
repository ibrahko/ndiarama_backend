from django.contrib import admin
from .models import Service
from apps.accounts.permissions import RoleBasedAdminMixin


@admin.register(Service)
class ServiceAdmin(RoleBasedAdminMixin):
    list_display = (
        "title",
        "category",
        "order",
        "is_active",
        "is_highlighted",
        "created_at",
    )
    list_filter = ("category", "is_active", "is_highlighted")
    search_fields = ("title", "short_description", "description")
    prepopulated_fields = {"slug": ("title",)}
    ordering = ("category", "order", "title")