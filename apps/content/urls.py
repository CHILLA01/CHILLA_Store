from django.urls import path
from .views import (
    CategoryListCreateView,
    CategoryDetailView,
    ModelListCreateView,
    ModelDetailView,
)

urlpatterns = [
    path('categories/', CategoryListCreateView.as_view(), name='category-list-create'),
    path('categories/<int:pk>/', CategoryDetailView.as_view(), name='category-detail'),
    path('models/', ModelListCreateView.as_view(), name='model-list-create'),
    path('models/<int:pk>/', ModelDetailView.as_view(), name='model-detail'),
]
