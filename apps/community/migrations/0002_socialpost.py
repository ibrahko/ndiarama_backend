from django.db import migrations, models


class Migration(migrations.Migration):
    """Ajout du modele SocialPost pour la gestion des posts LinkedIn/TikTok depuis l'admin."""

    dependencies = [
        ("community", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="SocialPost",
            fields=[
                ("id",           models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ("platform",     models.CharField(choices=[("linkedin", "LinkedIn"), ("tiktok", "TikTok")], max_length=20)),
                ("excerpt",      models.TextField()),
                ("url",          models.URLField()),
                ("published_at", models.DateField()),
                ("likes",        models.PositiveIntegerField(default=0)),
                ("is_active",    models.BooleanField(default=True)),
                ("order",        models.PositiveIntegerField(default=0)),
                ("created_at",   models.DateTimeField(auto_now_add=True)),
                ("updated_at",   models.DateTimeField(auto_now=True)),
            ],
            options={"ordering": ["-published_at", "order"], "verbose_name": "Post reseaux sociaux", "verbose_name_plural": "Posts reseaux sociaux"},
        ),
    ]
