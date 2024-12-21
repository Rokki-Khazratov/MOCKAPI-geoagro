from django.db import models
from api.utils import LAND_TYPE, INVEST_TYPE, RESERVOIR_TYPE, TRELLIS_TYPE
from django.utils import timezone

from django.core.exceptions import ValidationError

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
    fertility_score = models.FloatField(
        null=True, 
        blank=True, 
        verbose_name="Унумдорлиги банитет балли",
        help_text="Балли унумдорлиги (1-100)"
    )
    land_type = models.CharField(max_length=10, choices=LAND_TYPE, verbose_name="Жойлашган тури")
    not_usable_area = models.FloatField(default=0, verbose_name="Непригодная площадь (га)")
    
    irrigation_systems_count = models.IntegerField(default=0, verbose_name="Қудуқлар сони")
    pump_station_count = models.IntegerField(default=0, verbose_name="Насос станцияси сони")
    reservoir_count = models.IntegerField(default=0, verbose_name="Ҳовузлар сони")
    
    fenced = models.BooleanField(default=False, verbose_name="Атрофи сетка билан ўралганлиги")
    is_fertile = models.BooleanField(default=True, verbose_name="Ҳосилли ёки ҳосилсиз")

    is_deleting = models.BooleanField(default=False, verbose_name="Ochirilishi kere")
    is_checked = models.BooleanField(default=False, verbose_name="Tekshirildi")
    prev_data = models.JSONField(null=True, blank=True, verbose_name="Предыдущие данные")

    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    def clean(self):
        """
        Validate the model fields before saving.
        """
        # Check for negative values in area fields
        if self.total_area < 0:
            raise ValidationError({'total_area': 'Общая площадь не может быть отрицательной.'})
        if self.irrigation_area < 0:
            raise ValidationError({'irrigation_area': 'Площадь ирригации не может быть отрицательной.'})
        if self.not_usable_area < 0:
            raise ValidationError({'not_usable_area': 'Непригодная площадь не может быть отрицательной.'})

        # Check irrigation_area does not exceed total_area
        if self.irrigation_area > self.total_area:
            raise ValidationError({'irrigation_area': 'Площадь ирригации не может превышать общую площадь.'})

        # Validate fertility_score
        if self.fertility_score is not None:
            if self.fertility_score < 1 or self.fertility_score > 100:
                raise ValidationError({'fertility_score': 'Балли унумдорлиги должна быть в диапазоне от 1 до 100.'})

        # Ensure total_area covers all sub-areas
        total_used_area = self.irrigation_area + self.not_usable_area + sum(
            fruit_area.area for fruit_area in self.fruit_areas.all()
        )
        if total_used_area > self.total_area:
            raise ValidationError('Сумма всех под-площадей превышает общую площадь.')


        # Validate fertility_score
        if self.fertility_score is not None and (self.fertility_score < 1 or self.fertility_score > 100):
            raise ValidationError({'fertility_score': 'Балли унумдорлиги должна быть в диапазоне от 1 до 100.'})

        # Validate not_usable_area
        if self.not_usable_area < 0:
            raise ValidationError({'not_usable_area': 'Непригодная площадь не может быть отрицательной.'})

        # Ensure total_area covers all sub-areas
        total_used_area = self.irrigation_area + self.not_usable_area + sum(
            fruit_area.area for fruit_area in self.fruit_areas.all()
        )
        if total_used_area > self.total_area:
            raise ValidationError("Сумма всех площадей превышает общую площадь.")

    @property
    def empty_area(self):
        """
        Calculate empty area: total_area - (irrigation_area + areas of all fruit areas + not_usable_area).
        """
        used_area = self.irrigation_area + self.not_usable_area + sum(
            fruit_area.area for fruit_area in self.fruit_areas.all()
        )
        return self.total_area - used_area

    def save(self, *args, **kwargs):
        """
        Validate and save the plantation data.
        """
        self.full_clean()  # Ensure model validation before saving
        super().save(*args, **kwargs)

    def clear_prev_data(self):
        """
        Clear previous data.
        """
        self.prev_data = None

    def __str__(self):
        return f"Plantation {self.id} ({self.district.name})"




class Farmer(models.Model):
    name = models.CharField(max_length=100, verbose_name="Фермер хўжалиги номи")
    founder_name = models.CharField(max_length=100, verbose_name="Таъсисчи ismi")
    director_name = models.CharField(max_length=100, verbose_name="Хўжалик директори")
    phone_number = models.CharField(max_length=20, verbose_name="Телефон рақами")
    address = models.TextField(verbose_name="Яшаш манзили")
    inn = models.CharField(max_length=20, verbose_name="Ташкилот ИНН")
    established_year = models.IntegerField(verbose_name="Ташкил этилган йил")
    email = models.EmailField(blank=True)

    def __str__(self):
        return f"{self.name}"

class Investment(models.Model):
    plantation = models.OneToOneField(Plantation, on_delete=models.CASCADE, related_name="investment")
    invest_type = models.CharField(max_length=10, choices=INVEST_TYPE, verbose_name="Маҳаллий ёки хорижий")
    investment_amount = models.FloatField(default=0, verbose_name="Хорижий инвестиция")

    def __str__(self):
        return f"Investment for Plantation {self.plantation.id} - {self.investment_amount}"

class Reservoir(models.Model):
    plantation = models.OneToOneField('Plantation', on_delete=models.CASCADE, related_name="reservoir")
    reservoir_type = models.CharField(max_length=50, choices=RESERVOIR_TYPE, verbose_name="Ҳовуз тури", null=True, blank=True)
    reservoir_volume = models.FloatField(null=True, blank=True, verbose_name="Ҳовуз ҳажми (м³)")  # Stored in cubic meters

    def __str__(self):
        return f"Reservoir for Plantation {self.plantation.id}"

class Trellis(models.Model):
    plantation = models.OneToOneField('Plantation', on_delete=models.CASCADE, related_name="trellis")
    trellis_installed_area = models.FloatField(default=0, verbose_name="Шпаллар ўрнатилган майдон")
    trellis_type = models.CharField(max_length=50, choices=TRELLIS_TYPE, verbose_name="Шпаллер тури", null=True, blank=True)
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
        return f"Subsidy for {self.plantation.farmer.name} ({self.year})"

class PlantationImage(models.Model):
    plantation = models.ForeignKey(Plantation, related_name="images", on_delete=models.CASCADE)
    image = models.ImageField(upload_to="plantation_images/", verbose_name="Расм")

    def __str__(self):
        return f"Image for Plantation {self.plantation.farmer.name}"


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

