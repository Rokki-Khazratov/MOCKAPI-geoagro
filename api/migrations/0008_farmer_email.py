# Generated by Django 4.2.17 on 2024-12-21 15:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_remove_investment_farm_type_investment_invest_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='farmer',
            name='email',
            field=models.EmailField(blank=True, max_length=254),
        ),
    ]
