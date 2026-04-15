from django.contrib import admin
from django.utils.html import format_html
from .models import Show, Episode
from apps.accounts.permissions import RoleBasedAdminMixin


class EpisodeInline(admin.TabularInline):
    model = Episode
    extra = 1
    fields = (
        "title",
        "slug",
        "media_type",
        "youtube_url",
        "media_url",
        "duration",
        "published_at",
        "is_published",
        "is_featured",
    )
    show_change_link = True


@admin.register(Show)
class ShowAdmin(RoleBasedAdminMixin):
    list_display = (
        "title", "tagline", "order",
        "is_active", "episode_count", "created_at"
    )
    list_editable = ["order", "is_active"]
    list_filter = ("is_active",)
    search_fields = ("title", "description")
    prepopulated_fields = {"slug": ("title",)}
    ordering = ("order", "title")
    inlines = [EpisodeInline]

    fieldsets = (
        ("Informations", {
            "fields": (
                "title", "slug", "tagline",
                "description", "image",
                "order", "is_active"
            )
        }),
        ("Plateformes de diffusion", {
            "fields": (
                "youtube_channel_url",
                "spotify_show_url",
                "apple_podcast_url"
            ),
            "description": "Liens vers les plateformes de diffusion du show"
        }),
    )

    def episode_count(self, obj):
        count = obj.episodes.filter(is_published=True).count()
        return f"{count} épisode(s)"
    episode_count.short_description = "Épisodes"


@admin.register(Episode)
class EpisodeAdmin(RoleBasedAdminMixin):
    list_display = (
        "title", "show", "media_type",
        "duration", "is_featured", "is_published",
        "published_at", "youtube_preview"
    )
    list_filter = ("media_type", "is_published", "is_featured", "show")
    search_fields = ("title", "description")
    list_editable = ["is_featured", "is_published"]
    prepopulated_fields = {"slug": ("title",)}
    date_hierarchy = "published_at"
    ordering = ("-published_at",)
    readonly_fields = ["youtube_preview_large", "youtube_video_id_display"]

    fieldsets = (
        ("Informations générales", {
            "fields": (
                "show", "title", "slug",
                "description", "thumbnail",
                "media_type", "duration",
                "published_at", "is_published", "is_featured"
            )
        }),
        ("YouTube", {
            "fields": (
                "youtube_url",
                "youtube_video_id_display",
                "youtube_preview_large",
            ),
            "description": "Collez l'URL YouTube complète, l'ID sera extrait automatiquement"
        }),
        ("Audio / Podcast", {
            "fields": (
                "media_url",
                "spotify_url",
                "apple_podcast_url"
            ),
            "description": "Liens vers les plateformes audio"
        }),
    )

    def youtube_preview(self, obj):
        if obj.youtube_video_id:
            return format_html(
                '<img src="https://img.youtube.com/vi/{}/default.jpg" '
                'style="height:40px;border-radius:4px;" />',
                obj.youtube_video_id
            )
        return "—"
    youtube_preview.short_description = "Aperçu"

    def youtube_preview_large(self, obj):
        if obj.youtube_embed_url:
            return format_html(
                '<iframe width="480" height="270" src="{}" '
                'frameborder="0" allowfullscreen '
                'style="border-radius:8px;"></iframe>',
                obj.youtube_embed_url
            )
        return "Aucune URL YouTube renseignée"
    youtube_preview_large.short_description = "Aperçu YouTube"

    def youtube_video_id_display(self, obj):
        vid_id = obj.youtube_video_id
        return vid_id if vid_id else "Non détecté"
    youtube_video_id_display.short_description = "ID YouTube extrait"