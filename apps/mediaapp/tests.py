"""
Tests de l'application mediaapp : émissions et épisodes.
"""
from django.core.cache import cache
from django.test import TestCase
from django.utils import timezone

from .models import Show, Episode

SHOWS_URL = "/api/media/shows/"
EPISODES_URL = "/api/media/episodes/"


def make_show(slug="del-podcast", active=True, **kwargs):
    return Show.objects.create(
        title=kwargs.pop("title", slug.upper()),
        slug=slug,
        is_active=active,
        **kwargs,
    )


def make_episode(show, slug, published=True, **kwargs):
    return Episode.objects.create(
        show=show,
        title=kwargs.pop("title", slug),
        slug=slug,
        media_type=kwargs.pop("media_type", "audio"),
        published_at=kwargs.pop("published_at", timezone.now()),
        is_published=published,
        **kwargs,
    )


class ShowApiTests(TestCase):
    def setUp(self):
        cache.clear()
        self.show = make_show("del-podcast")
        self.inactive = make_show("archive", active=False)

    def test_list_returns_only_active_shows(self):
        response = self.client.get(SHOWS_URL)

        self.assertEqual(response.status_code, 200)
        body = response.json()
        # Réponse paginée : {count, next, previous, results}
        self.assertIn("results", body)
        slugs = [s["slug"] for s in body["results"]]
        self.assertIn("del-podcast", slugs)
        self.assertNotIn("archive", slugs)

    def test_detail_by_slug(self):
        response = self.client.get(f"{SHOWS_URL}del-podcast/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["slug"], "del-podcast")

    def test_detail_inactive_show_is_404(self):
        response = self.client.get(f"{SHOWS_URL}archive/")
        self.assertEqual(response.status_code, 404)

    def test_nested_episodes_exclude_unpublished(self):
        make_episode(self.show, "ep-publie", published=True)
        make_episode(self.show, "ep-brouillon", published=False)

        response = self.client.get(f"{SHOWS_URL}del-podcast/")

        episodes = response.json()["episodes"]
        slugs = [e["slug"] for e in episodes]
        self.assertEqual(slugs, ["ep-publie"])

    def test_write_is_not_allowed(self):
        response = self.client.post(
            SHOWS_URL,
            {"title": "Hack", "slug": "hack"},
            content_type="application/json",
        )
        # ReadOnlyModelViewSet : méthode non autorisée
        self.assertEqual(response.status_code, 405)


class EpisodeApiTests(TestCase):
    def setUp(self):
        cache.clear()
        self.show = make_show("english-corner")
        self.other = make_show("del-podcast")
        make_episode(self.show, "lesson-1")
        make_episode(self.show, "lesson-2", published=False)
        make_episode(self.other, "interview-1")

    def test_list_excludes_unpublished(self):
        response = self.client.get(EPISODES_URL)

        results = response.json()["results"]
        slugs = [e["slug"] for e in results]
        self.assertIn("lesson-1", slugs)
        self.assertNotIn("lesson-2", slugs)

    def test_filter_by_show_slug(self):
        response = self.client.get(EPISODES_URL, {"show": "english-corner"})

        results = response.json()["results"]
        self.assertEqual([e["slug"] for e in results], ["lesson-1"])

    def test_episodes_of_inactive_show_are_hidden(self):
        self.other.is_active = False
        self.other.save()

        response = self.client.get(EPISODES_URL)

        slugs = [e["slug"] for e in response.json()["results"]]
        self.assertNotIn("interview-1", slugs)

    def test_youtube_id_extraction_exposed(self):
        make_episode(
            self.show,
            "video-ep",
            media_type="video",
            youtube_url="https://www.youtube.com/watch?v=abc123DEF45",
        )

        response = self.client.get(EPISODES_URL, {"show": "english-corner"})

        ep = next(
            e for e in response.json()["results"] if e["slug"] == "video-ep"
        )
        self.assertEqual(ep["youtube_video_id"], "abc123DEF45")
        self.assertEqual(
            ep["youtube_embed_url"], "https://www.youtube.com/embed/abc123DEF45"
        )
        self.assertTrue(ep["has_video"])
