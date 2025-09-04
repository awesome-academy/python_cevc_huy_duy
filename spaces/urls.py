from django.urls import path
from .views import (
    SpaceCreateView,
    SpaceListView,
    SpaceDetailView,
)

app_name = 'spaces'

urlpatterns = [
    path('', SpaceListView.as_view(), name='space-list'),
    path('create/', SpaceCreateView.as_view(), name='space-create'),
    path('<int:pk>/', SpaceDetailView.as_view(), name='space-detail'),
]
