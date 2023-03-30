# Generated by Django 4.1.4 on 2023-03-29 09:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0016_alter_documenttype_type_document'),
    ]

    operations = [
        migrations.AlterField(
            model_name='documenttype',
            name='type_document',
            field=models.CharField(blank=True, choices=[('DOGOVOR', 'Договор'), ('IDS', 'ИДС'), ('MEDCARD', 'Мед карта'), ('ADMCARD', 'Адм.карта'), ('RENT', 'Справка в налоговую'), ('PLAN', 'План лечения'), ('DNEVNIK', 'Дневник'), ('OTKAZ_OT_MED', 'Отказ от мед.вмешательства'), ('UVEDOMLENIE', 'Уведомление'), ('RECEPT', 'Рецепт'), ('RECOMEND', 'Рекомендация стоматолога'), ('LECHENIE_BEZ_GARANTIY', 'Согласие о лечении без гарантий')], max_length=240, null=True),
        ),
    ]