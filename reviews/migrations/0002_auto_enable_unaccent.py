# reviews/migrations/0002_auto_enable_unaccent.py
from django.db import migrations


def enable_unaccent(apps, schema_editor):
    with schema_editor.connection.cursor() as cursor:
        cursor.execute("CREATE EXTENSION IF NOT EXISTS unaccent;")


class Migration(migrations.Migration):
    dependencies = [
        ("reviews", "0002_initial"),
    ]

    operations = [
        migrations.RunPython(enable_unaccent),
    ]
