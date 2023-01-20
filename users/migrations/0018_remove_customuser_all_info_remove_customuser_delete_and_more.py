# Generated by Django 4.1.5 on 2023-01-20 02:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0017_remove_action_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='all_info',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='delete',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='documents',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='downloads',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='logs',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='my_info',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='pasports',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='phones',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='settings',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='views',
        ),
        migrations.AddField(
            model_name='customuser',
            name='date_of_birthday',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Дата Рождения'),
        ),
    ]
