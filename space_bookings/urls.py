from django.urls import path
from .views import (
    SpaceBookingCreateView,
    SpaceBookingListView,
    SpaceBookingDetailView,
    SpaceBookingCancelView
)

urlpatterns = [
    path(
        'bookings/',
        SpaceBookingCreateView.as_view(),
        name='space-booking-create'
    ),
    path(
        'bookings/list/',
        SpaceBookingListView.as_view(),
        name='space-booking-list'
    ),
    path(
        'bookings/<int:pk>/',
        SpaceBookingDetailView.as_view(),
        name='space-booking-detail'
    ),
    path(
        'bookings/<int:pk>/cancel/',
        SpaceBookingCancelView.as_view(),
        name='space-booking-cancel'
    ),
]
