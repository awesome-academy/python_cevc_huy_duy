from django.db import models
from django.contrib.auth.models import AbstractUser
from constants import UserStatusChoices


class User(AbstractUser):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    
    status = models.CharField(
        max_length=20,
        choices=UserStatusChoices.choices,
        default=UserStatusChoices.REGISTER
    )
    
    # Token fields for authentication
    auth_token = models.CharField(max_length=255, blank=True, null=True)
    refresh_token = models.CharField(max_length=255, blank=True, null=True)
    confirmation_token = models.CharField(max_length=255, blank=True, null=True)
    confirmation_sent_at = models.DateTimeField(blank=True, null=True)
    confirmed_at = models.DateTimeField(blank=True, null=True)
    reset_password_token = models.CharField(max_length=255, blank=True, null=True)
    reset_password_sent_at = models.DateTimeField(blank=True, null=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"
