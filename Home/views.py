from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from .models import Category
from .serializers import CategorySerializer
from rest_framework.decorators import action

class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.filter(is_deleted=False)  # Only fetch non-deleted categories
    serializer_class = CategorySerializer



    # def list(self, request, *args, **kwargs):

    #     queryset = self.get_queryset()  # Fetch the categories that are not marked as deleted
    #     serializer = self.get_serializer(queryset, many=True)
    #     return Response(serializer.data)
    def list(self, request, *args, **kwargs):
    # Fetch top-level categories only (categories without a parent)
        queryset = self.get_queryset().filter(parent__isnull=True)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)  

    def perform_destroy(self, instance):

        instance.is_deleted = True
        instance.save()

    @action(detail=True, methods=['get'], url_path='children')
    def get_children(self, request, pk=None):
        """Retrieve all non-deleted children of a specific category."""
        category = self.get_object()  # Get the specific category instance
        
        # Fetch non-deleted children using the related name 'children'
        children = category.children.filter(is_deleted=False)
        
        # Serialize the children data
        serializer = CategorySerializer(children, many=True)
        
        return Response(serializer.data)

    @action(detail=True, methods=['get'], url_path='children_data')
    def children_data(self, request, pk=None):
        category = self.get_object()  # Get the specific category instance
        
        serializer = self.get_serializer(category)  # Serialize the category including its data
        
        return Response({
            'id': serializer.data['id'],
            'name': serializer.data['name'],
            'is_deleted': serializer.data['is_deleted'],
            'children_data': serializer.data['children_data']  # Include children data here
        })
