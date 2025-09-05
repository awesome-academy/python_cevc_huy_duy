from rest_framework import serializers
from .models import Space
from working_spaces.models import WorkingSpace
from space_prices.models import SpacePrice
from constants.messages import SpaceMessages
from constants.models import PriceTypeChoices
from utils.validators import validate_required_string
from decimal import Decimal


class SpaceFilterSerializer(serializers.Serializer):
    search = serializers.CharField(required=False, allow_blank=True)
    status = serializers.CharField(required=False, allow_blank=True)
    space_type = serializers.CharField(required=False, allow_blank=True)
    working_space_id = serializers.IntegerField(required=False, min_value=1)
    is_approved = serializers.BooleanField(required=False)

    def get_cleaned_data(self):
        data = {}
        
        search = self.validated_data.get('search')
        if search and search.strip():
            data['search'] = search.strip()
            
        status = self.validated_data.get('status')
        if status and status.strip():
            data['status'] = status.strip()
            
        space_type = self.validated_data.get('space_type')
        if space_type and space_type.strip():
            data['space_type'] = space_type.strip()
            
        working_space_id = self.validated_data.get('working_space_id')
        if working_space_id is not None:
            data['working_space_id'] = working_space_id
            
        is_approved = self.validated_data.get('is_approved')
        if is_approved is not None:
            data['is_approved'] = is_approved
            
        return data


class SpaceListSerializer(serializers.ModelSerializer):
    working_space_name = serializers.CharField(source='working_space.name', read_only=True)
    working_space_city = serializers.CharField(source='working_space.city', read_only=True)

    class Meta:
        model = Space
        fields = [
            'id',
            'working_space_name',
            'working_space_city',
            'name',
            'status',
            'space_type',
            'capacity',
            'location',
            'is_approved',
            'created_at'
        ]


class SpaceSerializer(SpaceListSerializer):
    class Meta(SpaceListSerializer.Meta):
        fields = SpaceListSerializer.Meta.fields + [
            'working_space',
            'description',
            'open_time',
            'close_time',
            'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'working_space_name', 'working_space_city']

    @validate_required_string
    def validate_name(self, value):
        return value

    @validate_required_string
    def validate_location(self, value):
        return value

    def validate_working_space(self, value):
        if not WorkingSpace.objects.filter(id=value.id).exists():
            raise serializers.ValidationError(SpaceMessages.WORKING_SPACE_NOT_FOUND)
        return value

    def validate(self, attrs):
        open_time = attrs.get('open_time')
        close_time = attrs.get('close_time')
        
        if open_time and close_time and open_time >= close_time:
            raise serializers.ValidationError({
                'close_time': SpaceMessages.INVALID_TIME_RANGE
            })
        
        return attrs


class SpaceCreateSerializer(SpaceSerializer):
    def validate(self, attrs):
        attrs = super().validate(attrs)
        
        name = attrs.get('name', '').strip()
        working_space = attrs.get('working_space')
        
        if Space.objects.filter(
            name=name,
            working_space=working_space
        ).exists():
            raise serializers.ValidationError({
                'name': SpaceMessages.DUPLICATE_NAME_WORKING_SPACE
            })
        
        return attrs


class SpacePriceInputSerializer(serializers.Serializer):
    price_type = serializers.ChoiceField(choices=PriceTypeChoices.choices)
    price = serializers.DecimalField(max_digits=10, decimal_places=2, min_value=Decimal('0.01'))


class SpaceCreateWithPricesSerializer(SpaceCreateSerializer):
    prices = SpacePriceInputSerializer(many=True, required=True)
    
    class Meta(SpaceCreateSerializer.Meta):
        fields = SpaceCreateSerializer.Meta.fields + ['prices']
    
    def validate_prices(self, prices):
        if len(prices) != 3:
            raise serializers.ValidationError(SpaceMessages.PRICE_ALL_TYPES_REQUIRED)
        
        price_types = [price['price_type'] for price in prices]
        required_types = [PriceTypeChoices.HOUR, PriceTypeChoices.DAY, PriceTypeChoices.MONTH]
        
        if set(price_types) != set(required_types):
            raise serializers.ValidationError(SpaceMessages.PRICE_HOUR_DAY_MONTH_REQUIRED)
        
        if len(price_types) != len(set(price_types)):
            raise serializers.ValidationError(SpaceMessages.DUPLICATE_PRICE_TYPES)
        
        return prices
    
    def create(self, validated_data):
        prices_data = validated_data.pop('prices')
        space = super().create(validated_data)
        
        for price_data in prices_data:
            SpacePrice.objects.create(
                space=space,
                type=price_data['price_type'],
                price=price_data['price']
            )
        
        return space


class SpaceUpdateSerializer(SpaceSerializer):
    def validate(self, attrs):
        attrs = super().validate(attrs)
        
        name = attrs.get('name')
        working_space = attrs.get('working_space')
        
        if name and working_space:
            name = name.strip()
            existing_space = Space.objects.filter(
                name=name,
                working_space=working_space
            ).exclude(id=self.instance.id)
            
            if existing_space.exists():
                raise serializers.ValidationError({
                    'name': SpaceMessages.DUPLICATE_NAME_WORKING_SPACE
                })
        
        return attrs


class SpaceUpdateWithPricesSerializer(SpaceUpdateSerializer):
    prices = SpacePriceInputSerializer(many=True, required=False)
    
    class Meta(SpaceUpdateSerializer.Meta):
        fields = SpaceUpdateSerializer.Meta.fields + ['prices']
    
    def validate_prices(self, prices):
        if prices:
            if len(prices) != 3:
                raise serializers.ValidationError(SpaceMessages.PRICE_ALL_TYPES_REQUIRED)
            
            price_types = [price['price_type'] for price in prices]
            required_types = [PriceTypeChoices.HOUR, PriceTypeChoices.DAY, PriceTypeChoices.MONTH]
            
            if set(price_types) != set(required_types):
                raise serializers.ValidationError(SpaceMessages.PRICE_HOUR_DAY_MONTH_REQUIRED)
            
            if len(price_types) != len(set(price_types)):
                raise serializers.ValidationError(SpaceMessages.DUPLICATE_PRICE_TYPES)
        
        return prices
    
    def update(self, instance, validated_data):
        prices_data = validated_data.pop('prices', None)
        
        space = super().update(instance, validated_data)
        
        if prices_data is not None:
            SpacePrice.objects.filter(space=space).delete()
            
            for price_data in prices_data:
                SpacePrice.objects.create(
                    space=space,
                    type=price_data['price_type'],
                    price=price_data['price']
                )
        
        return space


class SpacePriceSerializer(serializers.ModelSerializer):
    price_type_display = serializers.CharField(source='get_type_display', read_only=True)
    
    class Meta:
        model = SpacePrice
        fields = ['type', 'price_type_display', 'price']


class SpaceWithPricesSerializer(SpaceSerializer):
    prices = SpacePriceSerializer(many=True, read_only=True)
    working_space_name = serializers.CharField(source='working_space.name', read_only=True)
    
    class Meta(SpaceSerializer.Meta):
        fields = SpaceSerializer.Meta.fields + ['prices', 'working_space_name']
