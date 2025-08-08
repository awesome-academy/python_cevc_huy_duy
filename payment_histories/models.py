from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal
from space_bookings.models import SpaceBooking
from space_members.models import SpaceMember
from constants import PaymentStatusChoices, PaymentTypeChoices, PaymentMethodChoices


class PaymentHistory(models.Model):
    space_booking = models.ForeignKey(
        SpaceBooking,
        on_delete=models.CASCADE,
        related_name='payment_histories'
    )
    space_member = models.ForeignKey(
        SpaceMember,
        on_delete=models.CASCADE,
        related_name='payment_histories',
        null=True,
        blank=True
    )
    
    status = models.CharField(
        max_length=20,
        choices=PaymentStatusChoices.choices,
        default=PaymentStatusChoices.PENDING
    )
    
    payment_type = models.CharField(
        max_length=20,
        choices=PaymentTypeChoices.choices,
        default=PaymentTypeChoices.NEW
    )
    
    payment_method = models.CharField(
        max_length=30,
        choices=PaymentMethodChoices.choices,
        default=PaymentMethodChoices.CREDIT_CARD
    )
    
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    
    order_id = models.CharField(max_length=100, unique=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Payment {self.order_id} - {self.amount} ({self.status})"
