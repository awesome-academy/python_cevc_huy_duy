from rest_framework import status, generics, permissions
from rest_framework.response import Response
from django.db.models import Q
from working_spaces.models import WorkingSpace
from .models import Space
from .serializers import (
    SpaceCreateWithPricesSerializer,
    SpaceWithPricesSerializer,
    SpaceUpdateWithPricesSerializer,
    SpaceListSerializer,
    SpaceFilterSerializer
)
from constants.messages import SpaceMessages


class SpaceCreateView(generics.CreateAPIView):
    serializer_class = SpaceCreateWithPricesSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        working_space_id = self.kwargs.get('working_space_id')
        
        if working_space_id:
            if not WorkingSpace.objects.filter(id=working_space_id).exists():
                return Response({
                    'error': SpaceMessages.WORKING_SPACE_NOT_FOUND
                }, status=status.HTTP_404_NOT_FOUND)
            
            data = request.data.copy()
            data['working_space'] = working_space_id
            serializer = self.get_serializer(data=data)
        else:
            return Response({
                'error': SpaceMessages.WORKING_SPACE_NOT_FOUND
            }, status=status.HTTP_404_NOT_FOUND)
        
        serializer.is_valid(raise_exception=True)
        space = serializer.save()

        response_serializer = SpaceWithPricesSerializer(space)
        return Response(
            {
                'message': SpaceMessages.CREATION_SUCCESS,
                'space': response_serializer.data
            },
            status=status.HTTP_201_CREATED
        )


class SpaceListView(generics.ListAPIView):
    serializer_class = SpaceListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        working_space_id = self.kwargs.get('working_space_id')
        
        if working_space_id:
            if not WorkingSpace.objects.filter(id=working_space_id).exists():
                return Space.objects.none()
            queryset = Space.objects.filter(working_space_id=working_space_id).order_by('-created_at')
        else:
            queryset = Space.objects.select_related('working_space').all().order_by('-created_at')
        
        filter_serializer = SpaceFilterSerializer(data=self.request.query_params)
        filter_serializer.is_valid(raise_exception=True)
        
        filters = filter_serializer.get_cleaned_data()
        
        search = filters.get('search')
        if search:
            if working_space_id:
                queryset = queryset.filter(
                    Q(name__icontains=search) |
                    Q(location__icontains=search) |
                    Q(description__icontains=search)
                )
            else:
                queryset = queryset.filter(
                    Q(name__icontains=search) |
                    Q(location__icontains=search) |
                    Q(working_space__name__icontains=search) |
                    Q(working_space__city__icontains=search) |
                    Q(description__icontains=search)
                )

        status_filter = filters.get('status')
        if status_filter:
            queryset = queryset.filter(status=status_filter)

        type_filter = filters.get('space_type')
        if type_filter:
            queryset = queryset.filter(space_type=type_filter)

        if not working_space_id:
            filter_working_space_id = filters.get('working_space_id')
            if filter_working_space_id:
                if WorkingSpace.objects.filter(id=filter_working_space_id).exists():
                    queryset = queryset.filter(working_space_id=filter_working_space_id)
                else:
                    queryset = queryset.none()

        is_approved = filters.get('is_approved')
        if is_approved is not None:
            queryset = queryset.filter(is_approved=is_approved)

        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response({
                'spaces': serializer.data
            })

        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'spaces': serializer.data,
            'count': queryset.count()
        }, status=status.HTTP_200_OK)


class SpaceDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        space_id = self.kwargs.get('pk')
        working_space_id = self.kwargs.get('working_space_id')
        
        if working_space_id:
            space = Space.objects.select_related('working_space').get(
                id=space_id, 
                working_space_id=working_space_id
            )
            return space


    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return SpaceUpdateWithPricesSerializer
        return SpaceWithPricesSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({
            'space': serializer.data
        }, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        
        url_working_space_id = self.kwargs.get('working_space_id')
        
        if url_working_space_id:
            data = request.data.copy()
            data.pop('working_space', None)
            
            if str(instance.working_space.id) != str(url_working_space_id):
                return Response({
                    'error': SpaceMessages.NOT_FOUND
                }, status=status.HTTP_400_BAD_REQUEST)
        else:
            data = request.data.copy()
            working_space_id = data.get('working_space')
            if working_space_id and str(working_space_id) != str(instance.working_space.id):
                if not WorkingSpace.objects.filter(id=working_space_id).exists():
                    return Response({
                        'error': SpaceMessages.WORKING_SPACE_NOT_FOUND
                    }, status=status.HTTP_404_NOT_FOUND)
        
        serializer = self.get_serializer(
            instance,
            data=data,
            partial=partial
        )
        serializer.is_valid(raise_exception=True)

        serializer.save()

        response_serializer = SpaceWithPricesSerializer(instance)
        return Response({
            'message': SpaceMessages.UPDATE_SUCCESS,
            'space': response_serializer.data
        }, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        
        url_working_space_id = self.kwargs.get('working_space_id')
        
        if url_working_space_id:
            if str(instance.working_space.id) != str(url_working_space_id):
                return Response({
                    'error': SpaceMessages.NOT_FOUND
                }, status=status.HTTP_400_BAD_REQUEST)
        
        if not WorkingSpace.objects.filter(id=instance.working_space.id).exists():
            return Response({
                'error': SpaceMessages.DELETE_WITH_DEPENDENCIES
            }, status=status.HTTP_400_BAD_REQUEST)

        instance.delete()

        return Response({
            'message': SpaceMessages.DELETE_SUCCESS
        }, status=status.HTTP_204_NO_CONTENT)

