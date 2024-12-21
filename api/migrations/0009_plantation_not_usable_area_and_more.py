# Generated by Django 4.2.17 on 2024-12-21 15:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_farmer_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='plantation',
            name='not_usable_area',
            field=models.FloatField(default=0, verbose_name='Непригодная площадь (га)'),
        ),
        migrations.AlterField(
            model_name='plantation',
            name='fertility_score',
            field=models.FloatField(blank=True, help_text='Балли унумдорлиги (1-100)', null=True, verbose_name='Унумдорлиги банитет балли'),
        ),
    ]