from django.contrib import admin


class RoleBasedAdminMixin(admin.ModelAdmin):
    """
    Règles simples :
    - superadmin / admin : full access
    - editor : lecture + ajout/modif de contenu, pas de suppression
    - viewer : lecture seule
    """

    def has_view_permission(self, request, obj=None):
        user = request.user
        if not user.is_authenticated:
            return False
        # Tout le monde connecté avec un rôle a la vue
        return user.is_superadmin() or user.is_admin() or user.is_editor() or user.is_viewer()

    def has_add_permission(self, request):
        user = request.user
        if not user.is_authenticated:
            return False
        return user.is_superadmin() or user.is_admin() or user.is_editor()

    def has_change_permission(self, request, obj=None):
        user = request.user
        if not user.is_authenticated:
            return False
        return user.is_superadmin() or user.is_admin() or user.is_editor()

    def has_delete_permission(self, request, obj=None):
        user = request.user
        if not user.is_authenticated:
            return False
        # Pas de delete pour editor
        return user.is_superadmin() or user.is_admin()