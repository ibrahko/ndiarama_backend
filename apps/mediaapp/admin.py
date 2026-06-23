"""
Admin Django — Application mediaapp.
"""
from dataclasses import dataclass
from django.contrib import admin
from django.utils.html import format_html
from unfold.admin import ModelAdmin, TabularInline
from unfold.decorators import display

from apps.accounts.permissions import RoleBasedAdminMixin
from .models import Show, Episode


@dataclass
class HeaderPhoto:
    path: str
    width: int | None = 44
    height: int | None = 44
    squared: bool = True
    borderless: bool = False
    as_background: bool = False


class EpisodeInline(TabularInline):
    model = Episode
    extra = 0
    show_change_link = True
    tab = True
    fields = (
        "title", "media_type", "youtube_url",
        "media_url", "duration", "published_at",
        "is_published", "is_featured",
    )
    verbose_name = "Episode"
    verbose_name_plural = "Episodes de cette emission"


@admin.register(Show)
class ShowAdmin(RoleBasedAdminMixin, ModelAdmin):
    compressed_fields = True
    list_display = ("display_show", "episode_count_badge", "order", "is_active_badge")
    list_display_links = ("display_show",)
    list_filter = ("is_active",)
    list_editable = ("order",)
    search_fields = ("title", "description")
    prepopulated_fields = {"slug": ("title",)}
    ordering = ("order", "title")
    inlines = [EpisodeInline]

    fieldsets = (
        ("Informations de l'emission", {
            "description": "Le titre et la description apparaissent sur la page Media du site.",
            "fields": ("title", "slug", "tagline", "description", "image"),
        }),
        ("Plateformes de diffusion", {
            "description": "Collez les liens vers vos pages sur chaque plateforme.",
            "fields": ("youtube_channel_url", "spotify_show_url", "apple_podcast_url"),
        }),
        ("Affichage", {
            "description": "Decochez 'Actif' pour masquer l'emission sans la supprimer.",
            "fields": ("order", "is_active"),
        }),
    )

    @display(description="Emission", header=True)
    def display_show(self, obj):
        photo = HeaderPhoto(path=obj.image.url) if obj.image else None
        return [obj.title, obj.tagline or "", None, photo]

    @display(description="Episodes publies")
    def episode_count_badge(self, obj):
        count = obj.episodes.filter(is_published=True).count()
        return format_html(
            '<span style="background:#cc8a5f;color:#fff;padding:2px 8px;'
            'border-radius:12px;font-size:11px;font-weight:600;">{} ep.</span>',
            count,
        )

    @display(description="Active", boolean=True)
    def is_active_badge(self, obj):
        return obj.is_active


@admin.register(Episode)
class EpisodeAdmin(RoleBasedAdminMixin, ModelAdmin):
    compressed_fields = True
    list_display = (
        "display_episode", "show", "media_type_badge",
        "duration", "is_featured", "is_published", "published_at",
    )
    list_display_links = ("display_episode",)
    list_filter = ("media_type", "is_published", "is_featured", "show")
    search_fields = ("title", "description")
    list_editable = ("is_featured", "is_published")
    prepopulated_fields = {"slug": ("title",)}
    date_hierarchy = "published_at"
    ordering = ("-published_at",)
    readonly_fields = ("youtube_preview_large", "youtube_video_id_display")

    fieldsets = (
        ("Informations de l'episode", {
            "description": "Le titre et la description apparaissent sur la page Media.",
            "fields": (
                "show", "title", "slug",
                "description", "thumbnail",
                "media_type", "duration", "published_at",
            ),
        }),
        ("YouTube", {
            "description": "Collez l'URL complete (ex: https://www.youtube.com/watch?v=abc123). L'ID est extrait automatiquement.",
            "fields": ("youtube_url", "youtube_video_id_display", "youtube_preview_large"),
        }),
        ("Audio / Podcast", {
            "description": "Liens vers les plateformes audio. Laissez vide si non applicable.",
            "fields": ("media_url", "spotify_url", "apple_podcast_url"),
        }),
        ("Visibilite", {
            "description": "Publie = visible sur le site. A la une = mis en avant page d'accueil.",
            "fields": ("is_published", "is_featured"),
        }),
    )

    @display(description="Episode", header=True)
    def display_episode(self, obj):
        if obj.youtube_video_id:
            photo = HeaderPhoto(
                path=f"https://img.youtube.com/vi/{obj.youtube_video_id}/mqdefault.jpg",
                width=64, height=36, squared=True,
            )
        elif obj.thumbnail:
            photo = HeaderPhoto(path=obj.thumbnail.url, width=64, height=36, squared=True)
        else:
            photo = None
        show_name = obj.show.title if obj.show else ""
        return [obj.title, show_name, None, photo]

    @display(description="Type")
    def media_type_badge(self, obj):
        colors = {"audio": "#2e7d32", "video": "#1565c0", "both": "#6a1b9a"}
        labels = {"audio": "Audio", "video": "Video", "both": "Les deux"}
        return format_html(
            '<span style="background:{};color:#fff;padding:2px 8px;'
            'border-radius:12px;font-size:11px;">{}</span>',
            colors.get(obj.media_type, "#555"),
            labels.get(obj.media_type, obj.media_type),
        )

    def youtube_preview_large(self, obj):
        if obj.youtube_embed_url:
            return format_html(
                '<iframe width="480" height="270" src="{}" frameborder="0" allowfullscreen '
                'style="border-radius:8px;margin-top:8px;"></iframe>',
                obj.youtube_embed_url,
            )
        return "Aucune URL YouTube renseignee."
    youtube_preview_large.short_description = "Apercu video"

    def youtube_video_id_display(self, obj):
        vid = obj.youtube_video_id
        if vid:
            return format_html(
                '<code style="background:#f3f4f6;padding:2px 6px;border-radius:4px;">{}</code>', vid
            )
        return "Non detecte — verifiez l'URL YouTube."
    youtube_video_id_display.short_description = "ID YouTube extrait"
