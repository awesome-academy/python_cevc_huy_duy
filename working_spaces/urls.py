from django.urls import path
from .views import (
    WorkingSpaceCreateView,
    WorkingSpaceListView,
    WorkingSpaceDetailView,
)

app_name = 'working_spaces'

urlpatterns = [
    path('', WorkingSpaceListView.as_view(), name='working-space-list'),
    path('create', WorkingSpaceCreateView.as_view(), name='working-space-create'),
    path('<int:pk>/', WorkingSpaceDetailView.as_view(), name='working-space-detail'),
]
