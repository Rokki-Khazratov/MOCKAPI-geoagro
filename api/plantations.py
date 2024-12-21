from rest_framework import serializers
from core.settings import BASE_URL
from .models import *
from .plantation_models import *

# Сериализаторы для Plantation

# Сериализатор для Subsidy
class SubsidySerializer(serializers.ModelSerializer):
    class Meta:
        model = Subsidy
        fields = ['id', 'plantation', 'year', 'contract_number', 'direction', 'amount', 'efficiency']


# Сериализатор для Trellis
class TrellisSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trellis
        fields = ['id', 'trellis_type', 'trellis_installed_area', 'trellis_count']



# Сериализатор для Rootstock
class RootstockSerializer(serializers.ModelSerializer):
    fruit_name = serializers.CharField(source='fruit.name', read_only=True)

    class Meta:
        model = Rootstock
        fields = ['id', 'name', 'fruit', 'fruit_name']


# Сериализатор для Reservoir
class ReservoirSerializer(serializers.ModelSerializer):
    reservoir_volume_in_cubic_meters = serializers.SerializerMethodField()

    class Meta:
        model = Reservoir
        fields = ['id', 'reservoir_type', 'reservoir_volume', 'reservoir_volume_in_cubic_meters']

    def get_reservoir_volume_in_cubic_meters(self, obj):
        return f"{obj.reservoir_volume} м³" if obj.reservoir_volume else None




# Сериализатор для Investment
class InvestmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Investment
        fields = ['id', 'plantation', 'farm_type', 'investment_foreign', 'investment_local']


# Сериализатор для Farmer
class FarmerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Farmer
        fields = ['id', 'name', 'founder_name', 'director_name', 'phone_number', 'address', 'inn', 'established_year']

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
    name = serializers.SerializerMethodField()

    class Meta:
        model = Plantation
        fields = ['id', 'name', 'coordinates','is_fertile']

    def get_name(self, obj):
        """
        Возвращает имя фермера, если оно существует.
        """
        return obj.farmer.name if obj.farmer else None



#! LOGIC

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
    empty_area = serializers.FloatField(read_only=True)

    class Meta:
        model = Plantation
        fields = [
            'id', 'garden_established_year', 'total_area', 'irrigation_area', 'fertility_score',
            'land_type', 'is_fertile', 'fenced', 'irrigation_systems_count', 'pump_station_count',
            'reservoir_count', 'district', 'farmer', 'investment', 'reservoir', 'trellis',
            'fruit_areas', 'images', 'coordinates', 'subsidies', 'not_usable_area', 'empty_area',
        ]

    def get_district(self, obj):
        district = obj.district
        return {'name': district.name, 'region': district.region.name} if district else None

    def get_farmer(self, obj):
        farmer = obj.farmer
        return {
            'name': farmer.name,
            'founder_name': farmer.founder_name,
            'director_name': farmer.director_name,
            'phone_number': farmer.phone_number,
            'address': farmer.address,
            'inn': farmer.inn,
            'email': farmer.email,
            'established_year': farmer.established_year
        } if farmer else None

    def get_investment(self, obj):
        investment = getattr(obj, 'investment', None)
        return {
            'invest_type': investment.invest_type,
            'investment_amount': investment.investment_amount
        } if investment else None

    def get_reservoir(self, obj):
        reservoir = getattr(obj, 'reservoir', None)
        return {
            'reservoir_type': reservoir.reservoir_type,
            'reservoir_volume': reservoir.reservoir_volume
        } if reservoir else None

    def get_trellis(self, obj):
        trellis = getattr(obj, 'trellis', None)
        return {
            'trellis_installed_area': trellis.trellis_installed_area,
            'trellis_type': trellis.trellis_type,
            'trellis_count': trellis.trellis_count
        } if trellis else None

    def get_subsidies(self, obj):
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




class PlantationCreateSerializer(serializers.ModelSerializer):
    coordinates = PlantationCoordinatesSerializer(many=True)
    fruit_areas = PlantationFruitAreaSerializer(many=True)
    images = serializers.ListField(child=serializers.ImageField())
    investment = serializers.JSONField()
    reservoir = serializers.JSONField()
    trellis = serializers.JSONField()

    class Meta:
        model = Plantation
        fields = [
            'garden_established_year', 'district', 'farmer', 'total_area', 'irrigation_area', 'fertility_score',
            'land_type', 'is_fertile', 'fenced', 'irrigation_systems_count', 'pump_station_count',
            'reservoir_count', 'coordinates', 'fruit_areas', 'images', 'investment', 'reservoir', 'trellis'
        ]

    def create(self, validated_data):
        coordinates_data = validated_data.pop('coordinates', [])
        fruit_areas_data = validated_data.pop('fruit_areas', [])
        images_data = validated_data.pop('images', [])
        investment_data = validated_data.pop('investment', {})
        reservoir_data = validated_data.pop('reservoir', {})
        trellis_data = validated_data.pop('trellis', {})

        plantation = Plantation.objects.create(**validated_data)

        for coord in coordinates_data:
            PlantationCoordinates.objects.create(plantation=plantation, **coord)

        for fruit_area in fruit_areas_data:
            PlantationFruitArea.objects.create(plantation=plantation, **fruit_area)

        for image in images_data:
            PlantationImage.objects.create(plantation=plantation, image=image)

        if investment_data:
            Investment.objects.create(plantation=plantation, **investment_data)

        if reservoir_data:
            Reservoir.objects.create(plantation=plantation, **reservoir_data)

        if trellis_data:
            Trellis.objects.create(plantation=plantation, **trellis_data)

        return plantation


