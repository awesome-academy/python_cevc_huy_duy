from django.db import models
from working_spaces.models import WorkingSpace
from constants import AmenityStatusChoices


class Amenity(models.Model):
    working_space = models.ForeignKey(
        WorkingSpace,
        on_delete=models.CASCADE,
        related_name='amenities'
    )
    name = models.CharField(max_length=200)
    
    status = models.CharField(
        max_length=20,
        choices=AmenityStatusChoices.choices,
        default=AmenityStatusChoices.WAITING
    )
    
    is_approved = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = "Amenities"
    
    def __str__(self):
        return f"{self.name} - {self.working_space.name}"
