from django.db import migrations


class Migration(migrations.Migration):
    """
    Aligne la valeur de la categorie 'training' → 'formation'
    pour correspondre au type ServiceCategory du frontend React.
    """

    dependencies = [
        ("services", "0001_initial"),
    ]

    operations = [
        # 1. Mettre a jour les donnees existantes en base
        migrations.RunSQL(
            sql="UPDATE services_service SET category = 'formation' WHERE category = 'training';",
            reverse_sql="UPDATE services_service SET category = 'training' WHERE category = 'formation';",
        ),
        # 2. Mettre a jour la contrainte de validation du champ
        migrations.AlterField(
            model_name="service",
            name="category",
            field=__import__("django.db.models", fromlist=["CharField"]).CharField(
                choices=[
                    ("consulting", "Consulting"),
                    ("program", "Programme"),
                    ("formation", "Formation"),
                ],
                max_length=20,
            ),
        ),
    ]
