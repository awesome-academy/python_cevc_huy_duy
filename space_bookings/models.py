from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator
from decimal import Decimal
from spaces.models import Space
from constants import BookingStatusChoices, PriceTypeChoices


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
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user} - {self.space} ({self.start_time} to {self.end_time})"
