from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrReadOnly(BasePermission):
    """
    - GET/HEAD/OPTIONS : ouvert (lecture publique)
    - POST/PUT/PATCH/DELETE : réservé admin/superadmin/editor
    """

    def has_permission(self, request, view):
        user = request.user
        if request.method in SAFE_METHODS:
            return True

        if not user.is_authenticated:
            return False

        return (
            getattr(user, "is_superadmin", lambda: False)()
            or getattr(user, "is_admin", lambda: False)()
            or getattr(user, "is_editor", lambda: False)()
        )


class IsAdminOnly(BasePermission):
    """
    CRUD réservé aux admins/superadmins.
    (pour endpoints sensibles genre gestion d’utilisateurs)
    """

    def has_permission(self, request, view):
        user = request.user
        if not user.is_authenticated:
            return False

        return (
            getattr(user, "is_superadmin", lambda: False)()
            or getattr(user, "is_admin", lambda: False)()
        )