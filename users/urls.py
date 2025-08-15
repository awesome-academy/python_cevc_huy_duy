from django.urls import path
from .views import (
    UserRegistrationView,
    EmailConfirmationView,
    ResendConfirmationView,
    LoginView,
    LogoutView,
    ProfileView,
)

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='user-register'),
    path('confirm-email/', EmailConfirmationView.as_view(), name='email-confirm'),
    path('resend-confirmation/', ResendConfirmationView.as_view(), name='resend-confirmation'),
    path('login/', LoginView.as_view(), name='user-login'),
    path('logout/', LogoutView.as_view(), name='user-logout'),
    path('profile/', ProfileView.as_view(), name='user-profile'),
]
