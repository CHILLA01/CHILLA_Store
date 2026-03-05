from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view
from .models import Category, Model
from .serializers import CategorySerializer, ModelReadSerializer, ModelWriteSerializer


@extend_schema_view(
    get=extend_schema(summary="List all categories", tags=["Categories"]),
    post=extend_schema(summary="Create a category", tags=["Categories"]),
)
class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']


@extend_schema_view(
    get=extend_schema(summary="Retrieve a category", tags=["Categories"]),
    put=extend_schema(summary="Update a category", tags=["Categories"]),
    patch=extend_schema(summary="Partial update a category", tags=["Categories"]),
    delete=extend_schema(summary="Delete a category", tags=["Categories"]),
)
class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


@extend_schema_view(
    get=extend_schema(summary="List all models", tags=["Models"]),
    post=extend_schema(summary="Create a model", tags=["Models"]),
)
class ModelListCreateView(generics.ListCreateAPIView):
    queryset = Model.objects.select_related('category').all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category']
    search_fields = ['name', 'description']
    ordering_fields = ['price', 'name']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ModelWriteSerializer
        return ModelReadSerializer


@extend_schema_view(
    get=extend_schema(summary="Retrieve a model", tags=["Models"]),
    put=extend_schema(summary="Update a model", tags=["Models"]),
    patch=extend_schema(summary="Partial update a model", tags=["Models"]),
    delete=extend_schema(summary="Delete a model", tags=["Models"]),
)
class ModelDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Model.objects.select_related('category').all()

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return ModelWriteSerializer
        return ModelReadSerializer
