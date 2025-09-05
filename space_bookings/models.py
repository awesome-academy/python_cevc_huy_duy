from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from django.utils import timezone
from decimal import Decimal
from spaces.models import Space
from space_prices.models import SpacePrice
from constants.models import BookingStatusChoices, PriceTypeChoices
from constants.messages import BookingMessages


class SpaceBooking(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='bookings'
    )
    space = models.ForeignKey(
        Space,
        on_delete=models.CASCADE,
        related_name='bookings'
    )
    
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    
    status = models.CharField(
        max_length=20,
        choices=BookingStatusChoices.choices,
        default=BookingStatusChoices.PROCESSING
    )
    
    price_type = models.CharField(
        max_length=10,
        choices=PriceTypeChoices.choices
    )
    
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    
    notes = models.TextField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'status']),
            models.Index(fields=['space', 'start_time']),
            models.Index(fields=['status', 'created_at']),
        ]
    
    def get_space_price(self):
        try:
            space_price = SpacePrice.objects.get(
                space=self.space,
                type=self.price_type
            )
            return space_price.price
        except SpacePrice.DoesNotExist:
            raise ValidationError(BookingMessages.SPACE_NOT_FOUND)
    
    def clean(self):
        if self.start_time and self.end_time:
            if self.start_time >= self.end_time:
                raise ValidationError(BookingMessages.INVALID_TIME_RANGE)
            
            if self.start_time <= timezone.now():
                raise ValidationError(BookingMessages.PAST_START_TIME)
                
            overlapping_bookings = SpaceBooking.objects.filter(
                space=self.space,
                status__in=[BookingStatusChoices.PROCESSING, BookingStatusChoices.SUCCEEDED]
            ).exclude(pk=self.pk if self.pk else None)
            
            for booking in overlapping_bookings:
                if (self.start_time < booking.end_time and self.end_time > booking.start_time):
                    raise ValidationError(BookingMessages.TIME_SLOT_OVERLAP)
    
    def save(self, *args, **kwargs):
        if self.price is None and self.price_type and self.space:
            self.price = self.get_space_price()
        
        self.clean()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.user} - {self.space} ({self.start_time} to {self.end_time})"
