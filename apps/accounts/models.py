from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_SUPERADMIN = "superadmin"
    ROLE_ADMIN = "admin"
    ROLE_EDITOR = "editor"
    ROLE_VIEWER = "viewer"

    ROLE_CHOICES = (
        (ROLE_SUPERADMIN, "Super administrateur"),
        (ROLE_ADMIN, "Administrateur"),
        (ROLE_EDITOR, "Éditeur"),
        (ROLE_VIEWER, "Lecteur"),
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default=ROLE_ADMIN,
    )

    def is_superadmin(self):
        return self.role == self.ROLE_SUPERADMIN or self.is_superuser

    def is_admin(self):
        return self.role in {self.ROLE_SUPERADMIN, self.ROLE_ADMIN} or self.is_superuser

    def is_editor(self):
        return self.role in {
            self.ROLE_SUPERADMIN,
            self.ROLE_ADMIN,
            self.ROLE_EDITOR,
        } or self.is_superuser

    def is_viewer(self):
        return self.role == self.ROLE_VIEWER