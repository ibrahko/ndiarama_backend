from django.contrib import admin
from .models import NewsletterSubscriber, ContactMessage
from apps.accounts.permissions import RoleBasedAdminMixin


@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(RoleBasedAdminMixin):
    list_display = ("email", "first_name", "source", "created_at")
    list_filter = ("source",)
    search_fields = ("email", "first_name")
    ordering = ("-created_at",)


@admin.register(ContactMessage)
class ContactMessageAdmin(RoleBasedAdminMixin):
    list_display = ("name", "email", "subject", "handled", "created_at")
    list_filter = ("handled", "created_at")
    search_fields = ("name", "email", "subject", "message")
    ordering = ("-created_at",)