# Generated by Django 5.0.3 on 2024-03-18 13:01

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("duplicati", "0002_alter_run_unique_together"),
    ]

    operations = [
        migrations.AddField(
            model_name="run",
            name="report",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
    ]