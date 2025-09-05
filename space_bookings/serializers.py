from rest_framework import serializers
from django.utils import timezone
from django.db.models import Q
from .models import SpaceBooking
from spaces.models import Space
from spaces.serializers import SpaceSerializer
from users.serializers import UserSerializer
from space_prices.models import SpacePrice
from constants.models import BookingStatusChoices, PriceTypeChoices
from constants.messages import BookingMessages


class SpaceBookingCreateSerializer(serializers.ModelSerializer):
    price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    
    class Meta:
        model = SpaceBooking
        fields = [
            'space', 'start_time', 'end_time', 'price_type', 
            'price', 'notes'
        ]
    
    def validate_space(self, value):
        if value.is_approved:
            raise serializers.ValidationError(BookingMessages.SPACE_NOT_FOUND)
        return value
        
    def validate(self, data):
        start_time = data.get('start_time')
        end_time = data.get('end_time')
        space = data.get('space')
        price_type = data.get('price_type')
        
        if start_time and end_time:
            if start_time >= end_time:
                raise serializers.ValidationError(BookingMessages.INVALID_TIME_RANGE)
            
            if start_time <= timezone.now():
                raise serializers.ValidationError(BookingMessages.PAST_START_TIME)
                
            overlapping_bookings = SpaceBooking.objects.filter(
                space=space,
                status__in=[BookingStatusChoices.PROCESSING, BookingStatusChoices.SUCCEEDED],
                start_time__lt=end_time,
                end_time__gt=start_time
            )
            
            if overlapping_bookings.exists():
                raise serializers.ValidationError(BookingMessages.TIME_SLOT_OVERLAP)
        
        if space and price_type:
            if not SpacePrice.objects.filter(space=space, type=price_type).exists():
                raise serializers.ValidationError(BookingMessages.SPACE_NOT_FOUND)
        
        return data
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class SpaceBookingUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpaceBooking
        fields = [
            'start_time', 'end_time', 'price_type', 
            'price', 'notes', 'status'
        ]
        
    def validate(self, data):
        start_time = data.get('start_time', self.instance.start_time)
        end_time = data.get('end_time', self.instance.end_time)
        
        if start_time and end_time:
            if start_time >= end_time:
                raise serializers.ValidationError(BookingMessages.INVALID_TIME_RANGE)
            
            if start_time <= timezone.now():
                raise serializers.ValidationError(BookingMessages.PAST_START_TIME)
                
            overlapping_bookings = SpaceBooking.objects.filter(
                space=self.instance.space,
                status__in=[BookingStatusChoices.PROCESSING, BookingStatusChoices.SUCCEEDED],
                start_time__lt=end_time,
                end_time__gt=start_time
            ).exclude(pk=self.instance.pk)
            
            if overlapping_bookings.exists():
                raise serializers.ValidationError(BookingMessages.TIME_SLOT_OVERLAP)
        
        return data


class SpaceBookingSerializer(serializers.ModelSerializer):
    space = SpaceSerializer(read_only=True)
    user = UserSerializer(read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    price_type_display = serializers.CharField(source='get_price_type_display', read_only=True)
    
    class Meta:
        model = SpaceBooking
        fields = [
            'id', 'user', 'space', 'start_time', 'end_time', 
            'status', 'status_display', 'price_type', 'price_type_display',
            'price', 'notes', 'created_at', 'updated_at'
        ]


class SpaceBookingListSerializer(serializers.ModelSerializer):
    space_name = serializers.CharField(source='space.name', read_only=True)
    space_id = serializers.IntegerField(source='space.id', read_only=True)
    working_space_name = serializers.CharField(source='space.working_space.name', read_only=True)
    user_email = serializers.CharField(source='user.email', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    price_type_display = serializers.CharField(source='get_price_type_display', read_only=True)
    
    class Meta:
        model = SpaceBooking
        fields = [
            'id', 'user_email', 'space_id', 'space_name', 'working_space_name',
            'start_time', 'end_time', 'status', 'status_display', 
            'price_type', 'price_type_display', 'price', 'created_at'
        ]


class SpaceBookingFilterSerializer(serializers.Serializer):
    status = serializers.ChoiceField(
        choices=BookingStatusChoices.choices,
        required=False
    )
    price_type = serializers.ChoiceField(
        choices=PriceTypeChoices.choices,
        required=False
    )
    space_id = serializers.IntegerField(required=False)
    working_space_id = serializers.IntegerField(required=False)
    start_date = serializers.DateField(required=False)
    end_date = serializers.DateField(required=False)
    user_id = serializers.IntegerField(required=False)
    search = serializers.CharField(required=False, max_length=255)
    
    def validate(self, data):
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        
        if start_date and end_date and start_date > end_date:
            raise serializers.ValidationError(BookingMessages.INVALID_DATE_RANGE)
            
        return data
    
    def get_cleaned_data(self):
        return {key: value for key, value in self.validated_data.items() if value is not None}
