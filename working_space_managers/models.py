from django.db import models
from django.conf import settings
from working_spaces.models import WorkingSpace
from constants import WorkingSpaceManagerRoleChoices


class WorkingSpaceManager(models.Model):
    working_space = models.ForeignKey(
        WorkingSpace,
        on_delete=models.CASCADE,
        related_name='managers'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='managed_spaces'
    )
    
    role = models.CharField(
        max_length=20,
        choices=WorkingSpaceManagerRoleChoices.choices,
        default=WorkingSpaceManagerRoleChoices.MANAGER
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['working_space', 'user']
    
    def __str__(self):
        return f"{self.user} - {self.working_space} ({self.role})"
