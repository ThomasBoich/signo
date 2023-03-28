# Generated by Django 4.1.4 on 2023-03-14 07:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0012_alter_documenttype_type_document'),
    ]

    operations = [
        migrations.AlterField(
            model_name='documenttype',
            name='type_document',
            field=models.CharField(blank=True, choices=[('DOGOVOR', 'Договор'), ('IDS', 'ИДС'), ('MEDCARD', 'Мед карта'), ('ADMCARD', 'Адм.карта'), ('RENT', 'Справка в налоговую'), ('PLAN', 'План лечения'), ('DNEVNIK', 'Дневник'), ('UVEDOMLENIE', 'Уведомление'), ('RECEPT', 'Рецепт'), ('RECOMEND', 'Рекомендация стоматолога'), ('OTKAZ', 'Отказ от мед.вмешательства')], max_length=240, null=True),
        ),
    ]