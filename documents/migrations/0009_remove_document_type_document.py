# Generated by Django 4.1.4 on 2023-01-07 09:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0008_alter_document_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='document',
            name='type_document',
        ),
    ]
