# Generated by Django 4.1.3 on 2022-11-17 09:10

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="customuser",
            name="addres",
            field=models.CharField(
                blank=True, max_length=240, verbose_name="Адрес пользователя"
            ),
        ),
        migrations.AddField(
            model_name="customuser",
            name="ban",
            field=models.BooleanField(default=False, verbose_name="Уволен"),
        ),
        migrations.AddField(
            model_name="customuser",
            name="first_name",
            field=models.CharField(
                blank=True, max_length=100, null=True, verbose_name="Имя"
            ),
        ),
        migrations.AddField(
            model_name="customuser",
            name="is_admin",
            field=models.BooleanField(default=False, verbose_name="Администратор"),
        ),
        migrations.AddField(
            model_name="customuser",
            name="last_name",
            field=models.CharField(
                blank=True, max_length=100, null=True, verbose_name="Фамилия"
            ),
        ),
        migrations.AddField(
            model_name="customuser",
            name="pasport_number",
            field=models.CharField(
                blank=True, max_length=12, verbose_name="Номер паспорта"
            ),
        ),
        migrations.AddField(
            model_name="customuser",
            name="pasport_series",
            field=models.CharField(
                blank=True, max_length=12, verbose_name="Серия паспорта"
            ),
        ),
        migrations.AddField(
            model_name="customuser",
            name="patronymic",
            field=models.CharField(
                blank=True, max_length=100, null=True, verbose_name="Отчество"
            ),
        ),
        migrations.AddField(
            model_name="customuser",
            name="phone",
            field=models.CharField(
                blank=True, max_length=12, null=True, verbose_name="Телефон"
            ),
        ),
        migrations.AddField(
            model_name="customuser",
            name="photo",
            field=models.ImageField(
                blank=True,
                default="media/users/use.png",
                upload_to="midia/users/%Y/%m/%d/",
                verbose_name="Аватар",
            ),
        ),
        migrations.AddField(
            model_name="customuser",
            name="type",
            field=models.CharField(
                choices=[("AD", "Администратор"), ("DO", "Доктор"), ("PA", "Пациент")],
                default="PA",
                max_length=6,
            ),
        ),
        migrations.AddField(
            model_name="customuser",
            name="user_profile_id",
            field=models.IntegerField(
                blank=True, null=True, verbose_name="ID пользователя"
            ),
        ),
        migrations.AlterField(
            model_name="customuser",
            name="date_joined",
            field=models.DateTimeField(
                blank=True,
                default=django.utils.timezone.now,
                null=True,
                verbose_name="date joined",
            ),
        ),
        migrations.AlterField(
            model_name="customuser",
            name="email",
            field=models.EmailField(
                max_length=254, unique=True, verbose_name="Логинус"
            ),
        ),
        migrations.AlterField(
            model_name="customuser",
            name="groups",
            field=models.ManyToManyField(
                blank=True,
                null=True,
                related_name="groups",
                to="auth.group",
                verbose_name="Группы",
            ),
        ),
        migrations.AlterField(
            model_name="customuser",
            name="is_active",
            field=models.BooleanField(default=True, verbose_name="Активирован"),
        ),
        migrations.AlterField(
            model_name="customuser",
            name="is_staff",
            field=models.BooleanField(default=False, verbose_name="staff status"),
        ),
        migrations.AlterField(
            model_name="customuser",
            name="is_superuser",
            field=models.BooleanField(default=False, verbose_name="super user"),
        ),
        migrations.AlterField(
            model_name="customuser",
            name="user_permissions",
            field=models.ManyToManyField(
                blank=True,
                null=True,
                related_name="user_permissions",
                to="auth.permission",
                verbose_name="Разрешения",
            ),
        ),
    ]
