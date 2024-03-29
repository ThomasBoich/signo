# Generated by Django 4.1.3 on 2022-11-17 14:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="DocumentsFiles",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("file", models.FileField(upload_to="documents/%Y/%m/%d/")),
            ],
        ),
        migrations.CreateModel(
            name="DocumentType",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(blank=True, max_length=240, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="Document",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "document",
                    models.FileField(
                        blank=True, null=True, upload_to="documents/%Y/%m/%d/"
                    ),
                ),
                (
                    "send_date",
                    models.DateTimeField(
                        auto_now_add=True, null=True, verbose_name="Дата отправки"
                    ),
                ),
                (
                    "sender_status",
                    models.BooleanField(blank=True, default=False, null=True),
                ),
                (
                    "recipient_status",
                    models.BooleanField(blank=True, default=False, null=True),
                ),
                (
                    "files",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="documents.documentsfiles",
                    ),
                ),
                (
                    "recipient",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="recipient",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Получатель",
                    ),
                ),
                (
                    "sender",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="sender",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Отправитель",
                    ),
                ),
                (
                    "type",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="documents.documenttype",
                    ),
                ),
            ],
            options={"verbose_name": "Документ", "verbose_name_plural": "Документы",},
        ),
    ]
