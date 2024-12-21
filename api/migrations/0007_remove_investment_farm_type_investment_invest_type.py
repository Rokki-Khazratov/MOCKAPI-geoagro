# Generated by Django 4.2.17 on 2024-12-21 15:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_rename_investment_foreign_investment_investment_amount_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='investment',
            name='farm_type',
        ),
        migrations.AddField(
            model_name='investment',
            name='invest_type',
            field=models.CharField(choices=[('махаллий', 'Махаллий'), ('xорожий', 'Хорожий')], max_length=10, verbose_name='Маҳаллий ёки хорижий'),
            preserve_default=False,
        ),
    ]