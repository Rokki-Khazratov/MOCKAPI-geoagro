from django.db import models
from api.utils import LAND_TYPE, FARM_TYPE
    
from django.db import models
from django.utils import timezone
from api.utils import LAND_TYPE, FARM_TYPE

class Plantation(models.Model):
    garden_established_year = models.IntegerField(verbose_name="Боғ барпо этилган йил", null=True, blank=True)
    district = models.ForeignKey('api.District', on_delete=models.CASCADE, verbose_name="Туман")    
    farmer = models.ForeignKey(
        'api.Farmer',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='plantations',
        verbose_name="Фермер"
    )
    total_area = models.FloatField(verbose_name="Жами ер майдони гектар")
    irrigation_area = models.FloatField(default=0, verbose_name="Томчилатиб суғориш майдони")
    fertility_score = models.FloatField(null=True, blank=True, verbose_name="Унумдорлиги банитет балли")  # 0 - 100
    land_type = models.CharField(max_length=10, choices=LAND_TYPE, verbose_name="Жойлашган тури")

    irrigation_systems_count = models.IntegerField(default=0, verbose_name="Қудуқлар сони")
    pump_station_count = models.IntegerField(default=0, verbose_name="Насос станцияси сони")
    reservoir_count = models.IntegerField(default=0, verbose_name="Ҳовузлар сони")
    
    fenced = models.BooleanField(default=False, verbose_name="Атрофи сетка билан ўралганлиги")
    is_fertile = models.BooleanField(default=True, verbose_name="Ҳосилли ёки ҳосилсиз")

    is_deleting = models.BooleanField(default=False, verbose_name="Ochirilishi kere")
    is_checked = models.BooleanField(default=False, verbose_name="Tekshirildi")
    prev_data = models.JSONField(null=True, blank=True, verbose_name="Предыдущие данные")

    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    def save(self, *args, **kwargs):
        """
        Проверяет изменения данных и обновляет prev_data. 
        Очищает prev_data, если данные подтверждены (is_checked=True).
        """
        if self.is_checked and self.prev_data:
            # Очищаем prev_data, если данные проверены
            self.clear_prev_data()

        if not self.pk or not self.is_checked:
            # Сбрасываем is_checked на False при любом изменении данных
            self.is_checked = False

        # Если объект уже существует, проверяем изменения
        if self.pk:
            original = Plantation.objects.get(pk=self.pk)
            changes = {}

            # Проверяем изменения в каждом поле
            for field in self._meta.get_fields():
                if field.concrete and field.name not in ['is_checked', 'prev_data']:
                    old_value = getattr(original, field.name)
                    new_value = getattr(self, field.name)

                    # Преобразуем связанные объекты в ID для сохранения
                    if field.name in ['district', 'farmer']:
                        old_value = old_value.id if old_value else None
                        new_value = new_value.id if new_value else None

                    if old_value != new_value:
                        changes[field.name] = {
                            'old': old_value,
                            'new': new_value
                        }

            # Сохраняем изменения в prev_data
            if changes:
                self.prev_data = changes
            else:
                self.prev_data = None  # Очищаем, если изменений нет

        super(Plantation, self).save(*args, **kwargs)

    def clear_prev_data(self):
        """
        Очищает данные из prev_data, если is_checked=True.
        """
        self.prev_data = None

    def __str__(self):
        return f"Plantation {self.id} - {self.district.name}"


class Farmer(models.Model):
    name = models.CharField(max_length=100, verbose_name="Фермер хўжалиги номи")
    founder_name = models.CharField(max_length=100, verbose_name="Таъсисчи ismi")
    director_name = models.CharField(max_length=100, verbose_name="Хўжалик директори")
    phone_number = models.CharField(max_length=20, verbose_name="Телефон рақами")
    address = models.TextField(verbose_name="Яшаш манзили")
    inn = models.CharField(max_length=20, verbose_name="Ташкилот ИНН")
    established_year = models.IntegerField(verbose_name="Ташкил этилган йил")

    def __str__(self):
        return f"{self.name}"

class Investment(models.Model):
    plantation = models.OneToOneField(Plantation, on_delete=models.CASCADE, related_name="investment")
    farm_type = models.CharField(max_length=10, choices=FARM_TYPE, verbose_name="Маҳаллий ёки интенсив")
    investment_foreign = models.FloatField(default=0, verbose_name="Хорижий инвестиция")
    investment_local = models.FloatField(default=0, verbose_name="Маҳаллий инвестиция")

    def __str__(self):
        return f"Investment for Plantation {self.plantation.id}"

class Reservoir(models.Model):
    plantation = models.OneToOneField(Plantation, on_delete=models.CASCADE, related_name="reservoir")
    reservoir_type = models.CharField(max_length=50, verbose_name="Ҳовуз тури", null=True, blank=True)
    reservoir_volume = models.FloatField(null=True, blank=True, verbose_name="Ҳовуз ҳажми")

    def __str__(self):
        return f"Reservoir for Plantation {self.plantation.id}"


class Trellis(models.Model):
    plantation = models.OneToOneField(Plantation, on_delete=models.CASCADE, related_name="trellis")
    trellis_installed_area = models.FloatField(default=0, verbose_name="Шпаллар ўрнатилган майдон")
    trellis_type = models.CharField(max_length=50, verbose_name="Шпаллер тури", null=True, blank=True)
    trellis_count = models.IntegerField(default=0, verbose_name="Шпаллар сони")

    def __str__(self):
        return f"Trellis for Plantation {self.plantation.id}"




class Subsidy(models.Model):
    plantation = models.ForeignKey(Plantation, related_name="subsidies", on_delete=models.CASCADE)
    year = models.IntegerField(verbose_name="Ажратилган йил")
    contract_number = models.CharField(max_length=50, verbose_name="Субсидия шартнома рақами")
    direction = models.CharField(max_length=100, verbose_name="Йўналиши")
    amount = models.FloatField(verbose_name="Миқдори сўм")
    efficiency = models.BooleanField(verbose_name="Самарадорлиги")

    def __str__(self):
        return f"Subsidy for {self.plantation.name} ({self.year})"

class PlantationImage(models.Model):
    plantation = models.ForeignKey(Plantation, related_name="images", on_delete=models.CASCADE)
    image = models.ImageField(upload_to="plantation_images/", verbose_name="Расм")

    def __str__(self):
        return f"Image for Plantation {self.plantation.name}"


class Fruits(models.Model):
    name = models.CharField(max_length=250, verbose_name="Мева номи")

    def __str__(self):
        return self.name
    

class FruitVariety(models.Model):
    fruit = models.ForeignKey(Fruits, on_delete=models.CASCADE, related_name='varieties', verbose_name="Мева")
    name = models.CharField(max_length=250, verbose_name="Нав номи")

    def __str__(self):
        return f"{self.fruit.name} - {self.name}"


class PlantationFruitArea(models.Model):
    plantation = models.ForeignKey(
        Plantation, 
        on_delete=models.CASCADE, 
        related_name="fruit_areas",
        verbose_name="Плантация"
    )
    fruit = models.ForeignKey(
        Fruits, 
        on_delete=models.CASCADE, 
        verbose_name="Мева тури"
    )
    variety = models.ForeignKey(
        FruitVariety, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        verbose_name="Нави"
    )
    rootstock = models.CharField(
        max_length=100, 
        verbose_name="Пайвантак номи", 
        null=True, 
        blank=True
    )
    planted_year = models.IntegerField(verbose_name="Экилган йили")
    area = models.FloatField(verbose_name="Экин ер майдони гектар")

    def __str__(self):
        return f"Fruit area in Plantation {self.plantation.id} - {self.fruit.name}"



class PlantationCoordinates(models.Model):
    plantation = models.ForeignKey(Plantation, related_name='coordinates', on_delete=models.CASCADE)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return f"Coordinates for Plantation {self.plantation.id}"

