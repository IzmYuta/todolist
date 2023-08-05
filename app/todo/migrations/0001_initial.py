# Generated by Django 4.2.1 on 2023-07-26 09:40

import uuid

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Todo",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("uid", models.CharField(max_length=100)),
                ("title", models.CharField(max_length=100)),
                (
                    "status",
                    models.CharField(
                        choices=[("new", "未着手"), ("wip", "着手中"), ("done", "完了")],
                        default="new",
                        max_length=10,
                    ),
                ),
                ("deadline", models.DateTimeField(blank=True, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
