from rest_framework import serializers
from core.settings import BASE_URL
from .models import *
from .plantation_models import *


# Сериализатор для изображений
class PlantationImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlantationImage
        fields = ['id', 'image']


# Сериализатор для координат
class PlantationCoordinatesSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlantationCoordinates
        fields = ['id', 'latitude', 'longitude']


# Сериализатор для фруктовых площадей
class PlantationFruitAreaSerializer(serializers.ModelSerializer):
    fruit_name = serializers.CharField(source='fruit.name', read_only=True)
    variety_name = serializers.CharField(source='variety.name', read_only=True)

    class Meta:
        model = PlantationFruitArea
        fields = ['id', 'fruit', 'fruit_name', 'variety', 'variety_name', 'rootstock', 'planted_year', 'area']


# Сериализатор для списка плантаций
class PlantationListSerializer(serializers.ModelSerializer):
    district_name = serializers.CharField(source='district.name', read_only=True)
    region_name = serializers.CharField(source='district.region.name', read_only=True)

    class Meta:
        model = Plantation
        fields = ['id', 'garden_established_year', 'district_name', 'region_name', 'total_area', 'is_deleting', 'is_checked','prev_data']


# Сериализатор для отображения на карте
class MapPlantationSerializer(serializers.ModelSerializer):
    coordinates = PlantationCoordinatesSerializer(many=True, read_only=True)

    class Meta:
        model = Plantation
        fields = ['id', 'garden_established_year', 'coordinates', 'is_fertile']


# Детализированный сериализатор плантации
class PlantationDetailSerializer(serializers.ModelSerializer):
    district = serializers.SerializerMethodField()
    farmer = serializers.SerializerMethodField()
    investment = serializers.SerializerMethodField()
    reservoir = serializers.SerializerMethodField()
    trellis = serializers.SerializerMethodField()
    fruit_areas = PlantationFruitAreaSerializer(many=True, read_only=True)
    images = PlantationImageSerializer(many=True, read_only=True)
    coordinates = PlantationCoordinatesSerializer(many=True, read_only=True)
    subsidies = serializers.SerializerMethodField()

    class Meta:
        model = Plantation
        fields = [
            'id', 'garden_established_year', 'total_area', 'irrigation_area', 'fertility_score',
            'land_type', 'is_fertile', 'fenced', 'irrigation_systems_count', 'pump_station_count',
            'reservoir_count', 'district', 'farmer', 'investment', 'reservoir', 'trellis',
            'fruit_areas', 'images', 'coordinates', 'subsidies',
        ]

    def get_district(self, obj):
        """Retrieve district and region details."""
        district = obj.district
        return {
            'name': district.name,
            'region': district.region.name
        } if district else None

    def get_farmer(self, obj):
        """Retrieve farmer details."""
        farmer = obj.farmer
        return {
            'name': farmer.name,
            'founder_name': farmer.founder_name,
            'director_name': farmer.director_name,
            'phone_number': farmer.phone_number,
            'address': farmer.address,
            'inn': farmer.inn,
            'established_year': farmer.established_year
        } if farmer else None

    def get_investment(self, obj):
        """Retrieve investment details."""
        investment = getattr(obj, 'investment', None)
        return {
            'invest_type': investment.invest_type,
            'investment_amount': investment.investment_amount,
        } if investment else None

    def get_reservoir(self, obj):
        """Retrieve reservoir details."""
        reservoir = getattr(obj, 'reservoir', None)
        return {
            'reservoir_type': reservoir.reservoir_type,
            'reservoir_volume': reservoir.reservoir_volume
        } if reservoir else None

    def get_trellis(self, obj):
        """Retrieve trellis details."""
        trellis = getattr(obj, 'trellis', None)
        return {
            'trellis_installed_area': trellis.trellis_installed_area,
            'trellis_type': trellis.trellis_type,
            'trellis_count': trellis.trellis_count
        } if trellis else None

    def get_subsidies(self, obj):
        """Retrieve subsidies details."""
        return [
            {
                'year': subsidy.year,
                'contract_number': subsidy.contract_number,
                'direction': subsidy.direction,
                'amount': subsidy.amount,
                'efficiency': 'Самарали' if subsidy.efficiency else 'Самарасиз'
            }
            for subsidy in obj.subsidies.all()
        ]




# Сериализатор для создания/обновления плантации
class PlantationCreateSerializer(serializers.ModelSerializer):
    coordinates = PlantationCoordinatesSerializer(many=True)
    fruit_areas = PlantationFruitAreaSerializer(many=True)
    images = serializers.ListField(child=serializers.ImageField())

    class Meta:
        model = Plantation
        fields = [
            'garden_established_year', 'district', 'total_area', 'irrigation_area', 'fertility_score',
            'land_type', 'is_fertile', 'fenced', 'irrigation_systems_count', 'pump_station_count',
            'reservoir_count', 'coordinates', 'fruit_areas', 'images',
        ]

    def create(self, validated_data):
        coordinates_data = validated_data.pop('coordinates', [])
        fruit_areas_data = validated_data.pop('fruit_areas', [])
        images_data = validated_data.pop('images', [])
        plantation = Plantation.objects.create(**validated_data)

        for coord in coordinates_data:
            PlantationCoordinates.objects.create(plantation=plantation, **coord)

        for fruit_area in fruit_areas_data:
            PlantationFruitArea.objects.create(plantation=plantation, **fruit_area)

        for image in images_data:
            PlantationImage.objects.create(plantation=plantation, image=image)

        return plantation

    def update(self, instance, validated_data):
        coordinates_data = validated_data.pop('coordinates', [])
        fruit_areas_data = validated_data.pop('fruit_areas', [])
        images_data = validated_data.pop('images', [])

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()

        # Обновляем связанные данные
        instance.coordinates.all().delete()
        for coord in coordinates_data:
            PlantationCoordinates.objects.create(plantation=instance, **coord)

        instance.fruit_areas.all().delete()
        for fruit_area in fruit_areas_data:
            PlantationFruitArea.objects.create(plantation=instance, **fruit_area)

        instance.images.all().delete()
        for image in images_data:
            PlantationImage.objects.create(plantation=instance, image=image)

        return instance
