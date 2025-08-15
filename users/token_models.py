from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class UserToken(models.Model):
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='auth_tokens'
    )
    access_token = models.TextField()
    refresh_token = models.TextField()
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'user_tokens'
        indexes = [
            models.Index(fields=['user', 'is_active']),
            models.Index(fields=['access_token']),
            models.Index(fields=['refresh_token']),
        ]

    def __str__(self):
        return f"Token for {self.user.email}: {self.access_token}"

    @classmethod
    def create_tokens_for_user(cls, user, access_token, refresh_token):
        return cls.objects.create(
            user=user,
            access_token=access_token,
            refresh_token=refresh_token,
        )


    @classmethod
    def is_token_valid(cls, access_token):
        try:
            token_obj = cls.objects.get(
                access_token=access_token,
                is_active=True
            )
            return token_obj.user
        except cls.DoesNotExist:
            return None
