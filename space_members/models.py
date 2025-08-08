from django.db import models
from django.conf import settings
from spaces.models import Space
from constants import MemberStatusChoices


class SpaceMember(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='space_members'
    )
    space = models.ForeignKey(
        Space,
        on_delete=models.CASCADE,
        related_name='space_members'
    )
    
    status = models.CharField(
        max_length=20,
        choices=MemberStatusChoices.choices,
        default=MemberStatusChoices.ACTIVE
    )

    join_time = models.DateTimeField()
    expired_time = models.DateTimeField()
    available_start_time = models.DateTimeField()
    available_end_time = models.DateTimeField()
    
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    
    def __str__(self):
        return f"{self.user} - {self.space}"
