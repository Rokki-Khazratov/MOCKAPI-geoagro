from api.plantation_models import * 
from django.db import models
from django.utils import timezone  
from datetime import date
from django.contrib.auth.models import AbstractUser


# UTILS 
class HealthStatus(models.TextChoices):
    YAHSHI = 'yahshi', 'Yahshi'
    ORTACHA = 'ortacha', 'Ortacha'
    YOMON = 'yomon', 'Yomon'

# MODELS
class Region(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class District(models.Model):
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.region} - {self.name}"




class CustomUser(AbstractUser):
    district = models.ForeignKey(District, related_name='users', on_delete=models.CASCADE, blank=True, null=True)
    phone_number = models.CharField(max_length=255)

    def has_permission_for_plantation(self, plantation):
        """Проверяет, имеет ли пользователь доступ к плантации."""
        return plantation.district == self.district

    def has_access_to_district(self, district):
        """
        Проверяет, есть ли у пользователя доступ к конкретному округу.
        """
        return district == self.district

    def __str__(self):
        return self.username   

