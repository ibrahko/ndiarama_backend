from django.contrib import admin
from .models import SiteSettings, TeamMember, Testimonial
from apps.accounts.permissions import RoleBasedAdminMixin


@admin.register(SiteSettings)
class SiteSettingsAdmin(RoleBasedAdminMixin):
    list_display = ("site_name", "email", "phone", "updated_at")
    fieldsets = (
        ("Identité", {"fields": ("site_name", "hero_slogan", "hero_video_url", "mission_text")}),
        ("Contact", {"fields": ("address", "email", "phone")}),
        ("Réseaux sociaux", {"fields": ("linkedin_url", "tiktok_url", "youtube_url")}),
    )

    def has_add_permission(self, request):
        # On limite à un seul enregistrement
        if SiteSettings.objects.exists():
            return False
        return super().has_add_permission(request)


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ("name", "role", "order", "is_active")
    list_filter = ("is_active",)
    search_fields = ("name", "role")
    ordering = ("order", "name")


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ("name", "position", "order", "is_active")
    list_filter = ("is_active",)
    search_fields = ("name", "position", "message")
    ordering = ("order", "name")