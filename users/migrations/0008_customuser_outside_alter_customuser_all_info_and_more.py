# Generated by Django 4.1.3 on 2022-11-18 03:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0007_custompermissions_customuser_all_info_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="customuser",
            name="outside",
            field=models.DateTimeField(
                blank=True, null=True, verbose_name="дата увольнения"
            ),
        ),
        migrations.AlterField(
            model_name="customuser",
            name="all_info",
            field=models.BooleanField(
                blank=True,
                default="True",
                null=True,
                verbose_name="Доступ к информации о всех пациентах",
            ),
        ),
        migrations.AlterField(
            model_name="customuser",
            name="delete",
            field=models.BooleanField(
                blank=True,
                default=True,
                null=True,
                verbose_name="Доступ к удалению документов",
            ),
        ),
        migrations.AlterField(
            model_name="customuser",
            name="documents",
            field=models.BooleanField(
                blank=True,
                default="True",
                null=True,
                verbose_name="Доступ к вкладке документы",
            ),
        ),
        migrations.AlterField(
            model_name="customuser",
            name="downloads",
            field=models.BooleanField(
                blank=True,
                default=True,
                null=True,
                verbose_name="Доступ к скачиванию документов",
            ),
        ),
        migrations.AlterField(
            model_name="customuser",
            name="logs",
            field=models.BooleanField(
                blank=True,
                default=True,
                null=True,
                verbose_name="Доступ к вкладке логи",
            ),
        ),
        migrations.AlterField(
            model_name="customuser",
            name="my_info",
            field=models.BooleanField(
                blank=True,
                default="True",
                null=True,
                verbose_name="Доступ к информации о своих пациентах",
            ),
        ),
        migrations.AlterField(
            model_name="customuser",
            name="pasports",
            field=models.BooleanField(
                blank=True,
                default=True,
                null=True,
                verbose_name="Доступ к паспортным данным",
            ),
        ),
        migrations.AlterField(
            model_name="customuser",
            name="phones",
            field=models.BooleanField(
                blank=True,
                default=True,
                null=True,
                verbose_name="Доступ к просмотру телефонов",
            ),
        ),
        migrations.AlterField(
            model_name="customuser",
            name="settings",
            field=models.BooleanField(
                blank=True,
                default="True",
                null=True,
                verbose_name="Доступ к вкладке настройка пользователей",
            ),
        ),
        migrations.AlterField(
            model_name="customuser",
            name="views",
            field=models.BooleanField(
                blank=True,
                default=True,
                null=True,
                verbose_name="Доступ к просмотру документов",
            ),
        ),
    ]
