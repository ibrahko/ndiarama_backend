"""
Admin Django — Application accounts.
"""
from dataclasses import dataclass
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.html import format_html
from unfold.admin import ModelAdmin
from unfold.forms import AdminPasswordChangeForm, UserChangeForm, UserCreationForm
from unfold.decorators import display

from .models import User


@dataclass
class HeaderPhoto:
    path: str
    width: int | None = 36
    height: int | None = 36
    squared: bool = False
    borderless: bool = False
    as_background: bool = False


def _initials(name: str) -> str:
    parts = (name or "").split()
    return "".join(p[0].upper() for p in parts[:2]) if parts else "?"


@admin.register(User)
class UserAdmin(DjangoUserAdmin, ModelAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm
    compressed_fields = True

    list_display = ("display_user", "email", "role_badge", "is_staff", "is_active_badge")
    list_display_links = ("display_user",)
    list_filter = ("role", "is_staff", "is_active")
    search_fields = ("username", "email", "first_name", "last_name")
    ordering = ("username",)

    fieldsets = (
        ("Identifiants", {
            "fields": ("username", "password"),
        }),
        ("Informations personnelles", {
            "fields": ("first_name", "last_name", "email"),
        }),
        ("Role et permissions", {
            "description": (
                "Super Admin : acces total. "
                "Admin : gestion du contenu et des utilisateurs. "
                "Editeur : peut modifier les contenus, pas les utilisateurs. "
                "Lecteur : acces en lecture seule."
            ),
            "fields": ("role", "is_active", "is_staff", "is_superuser"),
        }),
        ("Dates", {
            "fields": ("last_login", "date_joined"),
        }),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("username", "email", "password1", "password2", "role"),
        }),
    )

    @display(description="Utilisateur", header=True)
    def display_user(self, obj):
        full_name = obj.get_full_name() or obj.username
        return [full_name, obj.email, _initials(full_name), None]

    @display(description="Role")
    def role_badge(self, obj):
        colors = {
            "superadmin": "#b71c1c",
            "admin":      "#cc8a5f",
            "editor":     "#1565c0",
            "viewer":     "#555",
        }
        labels = {
            "superadmin": "Super Admin",
            "admin":      "Admin",
            "editor":     "Editeur",
            "viewer":     "Lecteur",
        }
        color = colors.get(obj.role, "#555")
        label = labels.get(obj.role, obj.role)
        return format_html(
            '<span style="background:{};color:#fff;padding:2px 8px;'
            'border-radius:12px;font-size:11px;">{}</span>',
            color, label,
        )

    @display(description="Actif", boolean=True)
    def is_active_badge(self, obj):
        return obj.is_active

    def has_view_permission(self, request, obj=None):
        return request.user.is_admin() or request.user.is_superadmin()

    def has_add_permission(self, request):
        return request.user.is_admin() or request.user.is_superadmin()

    def has_change_permission(self, request, obj=None):
        return request.user.is_admin() or request.user.is_superadmin()

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superadmin()
