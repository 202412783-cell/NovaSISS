from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('estudiantes', '0001_initial'),
    ]

    operations = [
        migrations.RunSQL(
            """
            CREATE TABLE IF NOT EXISTS "ESTUDIANTE" (
                id SERIAL PRIMARY KEY
            );
            """,
            reverse_sql="""
            DROP TABLE IF EXISTS "ESTUDIANTE";
            """
        ),
    ]