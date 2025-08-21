from rest_framework import status, generics, permissions
from rest_framework.response import Response
from django.db import IntegrityError
from django.db.models import Q
from django.http import Http404
from .models import WorkingSpace
from .serializers import (
    WorkingSpaceSerializer,
    WorkingSpaceCreateSerializer,
    WorkingSpaceListSerializer,
    WorkingSpaceFilterSerializer
)
from constants.messages import HTTPErrorMessages, WorkingSpaceMessages


class WorkingSpaceCreateView(generics.CreateAPIView):
    serializer_class = WorkingSpaceCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        working_space = serializer.save()

        response_serializer = WorkingSpaceSerializer(working_space)
        return Response(
            {
                'working_space': response_serializer.data
            },
            status=status.HTTP_201_CREATED
        )


class WorkingSpaceListView(generics.ListAPIView):
    serializer_class = WorkingSpaceListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = WorkingSpace.objects.all().order_by('-created_at')
        
        filter_serializer = WorkingSpaceFilterSerializer(data=self.request.query_params)
        filter_serializer.is_valid(raise_exception=True)
        
        filters = filter_serializer.get_cleaned_data()
        
        search = filters.get('search')
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(city__icontains=search) |
                Q(street__icontains=search)
            )

        city = filters.get('city')
        if city:
            queryset = queryset.filter(city__icontains=city)

        if all(k in filters for k in ['latitude', 'longitude', 'radius']):
            lat = filters['latitude']
            lng = filters['longitude']
            rad = filters['radius']
            
            lat_delta = rad / 111.0
            lng_delta = rad / (111.0 * abs(lat * 3.14159 / 180)) if lat != 0 else rad / 111.0

            queryset = queryset.filter(
                latitude__gte=lat - lat_delta,
                latitude__lte=lat + lat_delta,
                longitude__gte=lng - lng_delta,
                longitude__lte=lng + lng_delta
            )

        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response({
                'working_spaces': serializer.data
            })

        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'working_spaces': serializer.data,
            'count': queryset.count()
        }, status=status.HTTP_200_OK)


class WorkingSpaceDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = WorkingSpace.objects.all()
    serializer_class = WorkingSpaceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({
            'working_space': serializer.data
        }, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance,
            data=request.data,
            partial=partial
        )
        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response({
            'message': WorkingSpaceMessages.UPDATE_SUCCESS,
            'working_space': serializer.data
        }, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        # TODO: add remove relation when implement add spaces, amenities
        instance.delete()

        return Response({
            'message': WorkingSpaceMessages.DELETE_SUCCESS
        }, status=status.HTTP_204_NO_CONTENT)
