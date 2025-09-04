from django.db import models
from django.core.validators import MinValueValidator
from working_spaces.models import WorkingSpace
from constants.models import SpaceStatusChoices, SpaceTypeChoices


class Space(models.Model):
    working_space = models.ForeignKey(
        WorkingSpace,
        on_delete=models.CASCADE,
        related_name='spaces'
    )
    name = models.CharField(max_length=200)
    
    status = models.CharField(
        max_length=20,
        choices=SpaceStatusChoices.choices,
        default=SpaceStatusChoices.WAITING
    )
    
    space_type = models.CharField(
        max_length=20,
        choices=SpaceTypeChoices.choices,
        default=SpaceTypeChoices.WORKING_DESK
    )
    
    capacity = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        help_text="Maximum number of people"
    )
    description = models.TextField(blank=True)
    location = models.CharField(max_length=255)
    open_time = models.TimeField()
    close_time = models.TimeField()
    is_approved = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['working_space'], name='space_working_space_idx'),
            models.Index(fields=['working_space', 'name'], name='space_working_space_name_idx'),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=['working_space', 'name'],
                name='unique_space_name_per_working_space'
            )
        ]
    
    def __str__(self):
        return f"{self.name} - {self.working_space.name}"
