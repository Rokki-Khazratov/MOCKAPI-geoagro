from django.contrib import admin
from .models import *
from .plantation_models import *


# Inline admin для координат
class PlantationCoordinatesInline(admin.StackedInline):
    model = PlantationCoordinates
    extra = 1  # Количество пустых полей для добавления координат


# Inline admin для изображений
class PlantationImageInline(admin.StackedInline):
    model = PlantationImage
    extra = 1  # Количество пустых полей для добавления изображений


# Inline admin для площадей фруктов
class PlantationFruitAreaInline(admin.StackedInline):
    model = PlantationFruitArea
    extra = 1  # Количество пустых полей для добавления площади фрукта


@admin.register(PlantationCoordinates)
class PlantationCoordinatesAdmin(admin.ModelAdmin):
    list_display = ('id', 'plantation', 'latitude', 'longitude')


@admin.register(PlantationImage)
class PlantationImageAdmin(admin.ModelAdmin):
    list_display = ('image', 'plantation')


@admin.register(PlantationFruitArea)
class PlantationFruitAreaAdmin(admin.ModelAdmin):
    list_display = ('plantation', 'fruit', 'planted_year', 'area')


@admin.register(Farmer)
class FarmerAdmin(admin.ModelAdmin):
    list_display = ('name', 'founder_name', 'director_name', 'phone_number', 'inn', 'established_year')
    search_fields = ('name', 'founder_name', 'director_name', 'inn')


@admin.register(Investment)
class InvestmentAdmin(admin.ModelAdmin):
    list_display = ('plantation', 'farm_type', 'investment_foreign', 'investment_local')
    list_filter = ('farm_type',)
    search_fields = ('plantation__name',)


@admin.register(Reservoir)
class ReservoirAdmin(admin.ModelAdmin):
    list_display = ('plantation', 'reservoir_type', 'reservoir_volume')
    list_filter = ('reservoir_type',)
    search_fields = ('plantation__name',)


@admin.register(Trellis)
class TrellisAdmin(admin.ModelAdmin):
    list_display = ('plantation', 'trellis_installed_area', 'trellis_type', 'trellis_count')
    search_fields = ('plantation__name', 'trellis_type')


@admin.register(Subsidy)
class SubsidyAdmin(admin.ModelAdmin):
    list_display = ('plantation', 'year', 'contract_number', 'direction', 'amount', 'efficiency')
    list_filter = ('year', 'efficiency', 'direction')
    search_fields = ('plantation__name', 'contract_number', 'direction')


@admin.register(Plantation)
class PlantationAdmin(admin.ModelAdmin):
    list_display = ('id', 'district', 'garden_established_year', 'total_area', 'land_type')
    search_fields = ('district__name', 'land_type')
    list_filter = ('district', 'land_type', 'is_fertile')
    inlines = [PlantationCoordinatesInline, PlantationImageInline, PlantationFruitAreaInline]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs  # Суперпользователь видит все
        return qs.filter(district__users=request.user)


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    list_display = ('name', 'id', 'region')
    search_fields = ('name', 'region__name')
    list_filter = ('region',)


@admin.register(Fruits)
class FruitsAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
