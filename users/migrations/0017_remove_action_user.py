# Generated by Django 4.1.4 on 2023-01-17 12:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0016_remove_action_document_deleted_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='action',
            name='user',
        ),
    ]