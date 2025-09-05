from rest_framework import status, generics, permissions
from rest_framework.response import Response
from django.db.models import Q
from django.utils import timezone
from django.shortcuts import get_object_or_404
from .models import SpaceBooking
from .serializers import (
    SpaceBookingSerializer,
    SpaceBookingCreateSerializer,
    SpaceBookingUpdateSerializer,
    SpaceBookingListSerializer,
    SpaceBookingFilterSerializer
)
from constants.messages import BookingMessages
from constants.models import BookingStatusChoices

class SpaceBookingCreateView(generics.CreateAPIView):
    serializer_class = SpaceBookingCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        booking = serializer.save()

        response_serializer = SpaceBookingSerializer(booking)
        return Response(
            {
                'message': BookingMessages.CREATION_SUCCESS,
                'booking': response_serializer.data
            },
            status=status.HTTP_201_CREATED
        )


class SpaceBookingListView(generics.ListAPIView):
    serializer_class = SpaceBookingListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        
        if user.is_staff:
            queryset = SpaceBooking.objects.select_related(
                'user', 'space', 'space__working_space'
            ).all()
        else:
            queryset = SpaceBooking.objects.select_related(
                'user', 'space', 'space__working_space'
            ).filter(user=user)
        
        filter_serializer = SpaceBookingFilterSerializer(data=self.request.query_params)
        filter_serializer.is_valid(raise_exception=True)
        filters = filter_serializer.get_cleaned_data()
        
        space_id = filters.get('space_id')
        if space_id:
            queryset = queryset.filter(space_id=space_id)
        
        working_space_id = filters.get('working_space_id')
        if working_space_id:
            queryset = queryset.filter(space__working_space_id=working_space_id)
        
        search = filters.get('search')
        if search:
            queryset = queryset.filter(
                Q(space__name__icontains=search) |
                Q(space__working_space__name__icontains=search) |
                Q(user__email__icontains=search) |
                Q(notes__icontains=search)
            )
        
        status_filter = filters.get('status')
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        price_type_filter = filters.get('price_type')
        if price_type_filter:
            queryset = queryset.filter(price_type=price_type_filter)
        
        start_date = filters.get('start_date')
        end_date = filters.get('end_date')
        if start_date:
            queryset = queryset.filter(start_time__date__gte=start_date)
        if end_date:
            queryset = queryset.filter(end_time__date__lte=end_date)
        
        user_id_filter = filters.get('user_id')
        if user_id_filter and user.is_staff:
            queryset = queryset.filter(user_id=user_id_filter)
        
        return queryset.order_by('-created_at')

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response({
                'bookings': serializer.data
            })

        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'bookings': serializer.data,
            'count': queryset.count()
        }, status=status.HTTP_200_OK)


class SpaceBookingDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        booking_id = self.kwargs.get('pk')
        user = self.request.user
        
        filters = {'id': booking_id}
        
        if not user.is_staff:
            filters['user'] = user
        
        booking = get_object_or_404(
            SpaceBooking.objects.select_related('user', 'space', 'space__working_space'),
            **filters
        )
        
        return booking

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return SpaceBookingUpdateSerializer
        return SpaceBookingSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({
            'booking': serializer.data
        }, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        
        if instance.status == BookingStatusChoices.SUCCEEDED:
            if instance.start_time <= timezone.now():
                return Response({
                    'error': BookingMessages.CANNOT_MODIFY_COMPLETED
                }, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = self.get_serializer(
            instance,
            data=request.data,
            partial=partial
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({
            'message': BookingMessages.UPDATE_SUCCESS,
            'booking': SpaceBookingSerializer(instance).data
        }, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        
        if instance.start_time <= timezone.now():
            return Response({
                'error': BookingMessages.CANNOT_CANCEL_PAST
            }, status=status.HTTP_400_BAD_REQUEST)
        
        instance.delete()
        return Response({
            'message': BookingMessages.DELETE_SUCCESS
        }, status=status.HTTP_204_NO_CONTENT)


class SpaceBookingCancelView(generics.UpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        booking_id = self.kwargs.get('pk')
        user = self.request.user
        
        filters = {'id': booking_id}
        
        if not user.is_staff:
            filters['user'] = user
        
        booking = get_object_or_404(
            SpaceBooking.objects.select_related('user', 'space'),
            **filters
        )
        
        return booking
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        
        if instance.status == BookingStatusChoices.CANCELED:
            return Response({
                'error': BookingMessages.ALREADY_CANCELLED
            }, status=status.HTTP_400_BAD_REQUEST)
        
        if instance.start_time <= timezone.now():
            return Response({
                'error': BookingMessages.CANNOT_CANCEL_PAST
            }, status=status.HTTP_400_BAD_REQUEST)
        
        instance.status = BookingStatusChoices.CANCELED
        instance.save()
        
        return Response({
            'message': BookingMessages.CANCEL_SUCCESS,
            'booking': SpaceBookingSerializer(instance).data
        }, status=status.HTTP_200_OK)
