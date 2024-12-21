# Updated migration file: 0010_alter_plantation_land_type_and_more.py

from django.db import migrations, models
import django.db.models.deletion

def set_null_for_invalid_rootstock(apps, schema_editor):
    """
    Set rootstock to NULL for existing plantationfruitarea rows with invalid references.
    """
    PlantationFruitArea = apps.get_model('api', 'PlantationFruitArea')
    Rootstock = apps.get_model('api', 'Rootstock')

    # Get valid rootstock IDs
    valid_rootstock_ids = set(Rootstock.objects.values_list('id', flat=True))

    # Update rows with invalid rootstock references to NULL
    PlantationFruitArea.objects.filter(rootstock_id__isnull=False).exclude(rootstock_id__in=valid_rootstock_ids).update(rootstock_id=None)

class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_plantation_not_usable_area_and_more'),
    ]

    operations = [
        # Update field land_type in Plantation
        migrations.AlterField(
            model_name='plantation',
            name='land_type',
            field=models.CharField(
                choices=[
                    ('лялими', 'Лялими'),
                    ('тог олди', 'Тог олди'),
                    ('адир', 'Адир'),
                    ('сувли', 'Сувли майдон')
                ],
                max_length=10,
                verbose_name='Жойлашган тури'
            ),
        ),

        # Update reservoir_type in Reservoir
        migrations.AlterField(
            model_name='reservoir',
            name='reservoir_type',
            field=models.CharField(
                choices=[('beton', 'Beton'), ('qoplama', 'Qopлама')],
                max_length=50,
                null=True,
                blank=True,
                verbose_name='Ҳовуз тури'
            ),
        ),

        # Update reservoir_volume in Reservoir
        migrations.AlterField(
            model_name='reservoir',
            name='reservoir_volume',
            field=models.FloatField(
                null=True,
                blank=True,
                verbose_name='Ҳовуз ҳажми (м³)'
            ),
        ),

        # Update trellis_type in Trellis
        migrations.AlterField(
            model_name='trellis',
            name='trellis_type',
            field=models.CharField(
                choices=[('beton', 'Beton'), ('temir', 'Temir')],
                max_length=50,
                null=True,
                blank=True,
                verbose_name='Шпаллер тури'
            ),
        ),

        # Create Rootstock model
        migrations.CreateModel(
            name='Rootstock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Пайвантак номи')),
                ('fruit', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='rootstocks',
                    to='api.Fruits',
                    verbose_name='Мева тури'
                )),
            ],
        ),

        # Update rootstock field in PlantationFruitArea
        migrations.AlterField(
            model_name='plantationfruitarea',
            name='rootstock',
            field=models.ForeignKey(
                to='api.Rootstock',
                null=True,
                blank=True,
                on_delete=django.db.models.deletion.SET_NULL,
                verbose_name='Пайвантак номи'
            ),
        ),

        # Custom operation to clean up invalid data
        migrations.RunPython(set_null_for_invalid_rootstock, reverse_code=migrations.RunPython.noop),
    ]
