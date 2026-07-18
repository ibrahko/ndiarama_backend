"""
Tests de l'application core : settings du site, équipe, témoignages.
"""
from django.core.cache import cache
from django.test import TestCase

# Import via le module : pytest tenterait de collecter tout nom en Test*
from . import models as core_models
from .models import SiteSettings, TeamMember


class CoreApiTests(TestCase):
    def setUp(self):
        cache.clear()

    def test_site_settings_endpoint(self):
        SiteSettings.objects.create(
            site_name="NDIARAMA", email="contact@ndiarama.com"
        )

        response = self.client.get("/api/core/settings/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["site_name"], "NDIARAMA")

    def test_team_lists_only_active_members(self):
        TeamMember.objects.create(name="Actif", role="Fondateur")
        TeamMember.objects.create(name="Inactif", role="Ex", is_active=False)

        response = self.client.get("/api/core/team/")

        self.assertEqual(response.status_code, 200)
        names = [m["name"] for m in response.json()["results"]]
        self.assertEqual(names, ["Actif"])

    def test_testimonials_list_only_active(self):
        core_models.Testimonial.objects.create(name="Fatou", message="Top !")
        core_models.Testimonial.objects.create(
            name="Masqué", message="…", is_active=False
        )

        response = self.client.get("/api/core/testimonials/")

        names = [t["name"] for t in response.json()["results"]]
        self.assertEqual(names, ["Fatou"])
