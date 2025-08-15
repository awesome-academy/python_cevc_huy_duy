from django.urls import path
from .views import (
    UserRegistrationView,
    EmailConfirmationView,
    ResendConfirmationView
)

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='user-register'),
    path('confirm-email/', EmailConfirmationView.as_view(), name='email-confirm'),
    path('resend-confirmation', ResendConfirmationView.as_view(), name='resend-confirmation'),
]
