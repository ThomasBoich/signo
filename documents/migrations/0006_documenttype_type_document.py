# Generated by Django 4.1.3 on 2022-11-27 08:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("documents", "0005_document_founder"),
    ]

    operations = [
        migrations.AddField(
            model_name="documenttype",
            name="type_document",
            field=models.CharField(
                blank=True,
                choices=[
                    ("DOGOVOR", "Договор"),
                    ("IDS", "ИДС"),
                    ("MEDCARD", "Мед карта"),
                    ("ADMCARD", "Адм.карта"),
                    ("RENT", "Справка в налоговую"),
                    ("PLAN", "План лечения"),
                    ("DNEVNIK", "Дневник"),
                ],
                max_length=240,
                null=True,
            ),
        ),
    ]