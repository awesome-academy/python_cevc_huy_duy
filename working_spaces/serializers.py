from rest_framework import serializers
from .models import WorkingSpace
from constants.messages import WorkingSpaceMessages
from utils.validators import validate_required_string, validate_coordinate_range


class WorkingSpaceFilterSerializer(serializers.Serializer):
    search = serializers.CharField(required=False, allow_blank=True)
    city = serializers.CharField(required=False, allow_blank=True)
    latitude = serializers.FloatField(required=False)
    longitude = serializers.FloatField(required=False)
    radius = serializers.FloatField(required=False, min_value=0.01)

    @validate_coordinate_range(-90, 90)
    def validate_latitude(self, value):
        return value

    @validate_coordinate_range(-180, 180)
    def validate_longitude(self, value):
        return value

    def validate(self, attrs):
        latitude = attrs.get('latitude')
        longitude = attrs.get('longitude')
        radius = attrs.get('radius')

        location_params = [latitude, longitude, radius]
        provided_params = [p for p in location_params if p is not None]
        
        if 0 < len(provided_params) < 3:
            raise serializers.ValidationError(
                WorkingSpaceMessages.LOCATION_FILTER_INCOMPLETE
            )

        return attrs

    def get_cleaned_data(self):
        data = {}
        
        search = self.validated_data.get('search')
        if search and search.strip():
            data['search'] = search.strip()
            
        city = self.validated_data.get('city')
        if city and city.strip():
            data['city'] = city.strip()
            
        latitude = self.validated_data.get('latitude')
        longitude = self.validated_data.get('longitude')
        radius = self.validated_data.get('radius')
        
        if latitude is not None and longitude is not None and radius is not None:
            data['latitude'] = latitude
            data['longitude'] = longitude
            data['radius'] = radius
            
        return data


class WorkingSpaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkingSpace
        fields = [
            'id',
            'name',
            'city',
            'street',
            'latitude',
            'longitude',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    @validate_required_string
    def validate_name(self, value):
        return value

    @validate_required_string
    def validate_city(self, value):
        return value

    @validate_required_string
    def validate_street(self, value):
        return value

    @validate_coordinate_range(-90, 90)
    def validate_latitude(self, value):
        return value

    @validate_coordinate_range(-180, 180)
    def validate_longitude(self, value):
        return value


class WorkingSpaceCreateSerializer(WorkingSpaceSerializer):
    def validate(self, attrs):
        name = attrs.get('name', '').strip()
        city = attrs.get('city', '').strip()
        
        if WorkingSpace.objects.filter(
            name=name,
            city=city
        ).exists():
            raise serializers.ValidationError({
                'name': WorkingSpaceMessages.DUPLICATE_NAME_CITY
            })
        
        return attrs


class WorkingSpaceListSerializer(serializers.ModelSerializer):

    class Meta:
        model = WorkingSpace
        fields = [
            'id',
            'name',
            'city',
            'latitude',
            'longitude',
            'created_at'
        ]
