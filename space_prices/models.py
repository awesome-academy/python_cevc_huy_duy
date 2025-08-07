from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal
from spaces.models import Space
from constants import PriceTypeChoices


class SpacePrice(models.Model):
    space = models.ForeignKey(
        Space,
        on_delete=models.CASCADE,
        related_name='prices'
    )
    
    type = models.CharField(
        max_length=10,
        choices=PriceTypeChoices.choices,
        default=PriceTypeChoices.HOUR
    )
    
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['space', 'type']
    
    def __str__(self):
        return f"{self.space.name} - {self.type}: ${self.price}"
