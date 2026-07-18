"""
Tests des endpoints agrégés : /api/home/ et /api/health/.
"""
from django.core.cache import cache
from django.test import TestCase
from django.utils import timezone

# Import via le module pour éviter que pytest ne tente de collecter
# la classe "Testimonial" (tout nom commençant par "Test" est candidat).
from apps.core import models as core_models
from apps.core.models import SiteSettings, TeamMember
from apps.mediaapp.models import Show, Episode
from apps.services.models import Service

HOME_URL = "/api/home/"
HEALTH_URL = "/api/health/"


class HomeApiTests(TestCase):
    def setUp(self):
        cache.clear()
        SiteSettings.objects.create(hero_slogan="Inspirer, former, connecter")
        TeamMember.objects.create(name="Membre actif", role="Fondateur")
        TeamMember.objects.create(
            name="Ancien membre", role="Ex", is_active=False
        )
        core_models.Testimonial.objects.create(name="Fatou", message="Excellent !")

        show = Show.objects.create(title="DEL PODCAST", slug="del-podcast")
        Episode.objects.create(
            show=show,
            title="Épisode vedette",
            slug="ep-vedette",
            media_type="audio",
            published_at=timezone.now(),
            is_published=True,
            is_featured=True,
        )
        Episode.objects.create(
            show=show,
            title="Brouillon vedette",
            slug="ep-brouillon",
            media_type="audio",
            published_at=timezone.now(),
            is_published=False,
            is_featured=True,
        )

        Service.objects.create(
            category="formation",
            title="Formation soft skills",
            slug="soft-skills",
            is_highlighted=True,
        )
        Service.objects.create(
            category="consulting",
            title="Non mis en avant",
            slug="autre",
            is_highlighted=False,
        )

    def test_home_payload_structure(self):
        response = self.client.get(HOME_URL)

        self.assertEqual(response.status_code, 200)
        body = response.json()
        for key in (
            "settings",
            "team",
            "testimonials",
            "shows",
            "featured_episodes",
            "highlighted_services",
        ):
            self.assertIn(key, body)
        self.assertEqual(
            body["settings"]["hero_slogan"], "Inspirer, former, connecter"
        )

    def test_home_filters_inactive_and_unpublished(self):
        body = self.client.get(HOME_URL).json()

        team_names = [m["name"] for m in body["team"]]
        self.assertIn("Membre actif", team_names)
        self.assertNotIn("Ancien membre", team_names)

        featured_slugs = [e["slug"] for e in body["featured_episodes"]]
        self.assertEqual(featured_slugs, ["ep-vedette"])

        highlighted = [s["slug"] for s in body["highlighted_services"]]
        self.assertEqual(highlighted, ["soft-skills"])

    def test_home_nested_show_episodes_exclude_unpublished(self):
        body = self.client.get(HOME_URL).json()

        show = body["shows"][0]
        slugs = [e["slug"] for e in show["episodes"]]
        self.assertEqual(slugs, ["ep-vedette"])


class HealthApiTests(TestCase):
    def test_health_ok(self):
        response = self.client.get(HEALTH_URL)

        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertEqual(body["status"], "ok")
        self.assertTrue(body["database"])
