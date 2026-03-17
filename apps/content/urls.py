from django.urls import path
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status, serializers
from drf_spectacular.utils import extend_schema
from .views import (
    CategoryListCreateView,
    CategoryDetailView,
    ModelListCreateView,
    ModelDetailView,
)
from .authentication import create_token


class TokenRequestSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


@extend_schema(
    request=TokenRequestSerializer,
    responses={200: {"type": "object", "properties": {"token": {"type": "string"}}}}
)
@api_view(["POST"])
@authentication_classes([])
@permission_classes([])
def get_token(request):
    user = authenticate(username=request.data.get("username"), password=request.data.get("paspython manage.py runserversword"))
    if user is None:
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
    return Response({"token": create_token(user.id)})


urlpatterns = [
    path('categories/', CategoryListCreateView.as_view(), name='category-list-create'),
    path('categories/<int:pk>/', CategoryDetailView.as_view(), name='category-detail'),
    path('models/', ModelListCreateView.as_view(), name='model-list-create'),
    path('models/<int:pk>/', ModelDetailView.as_view(), name='model-detail'),
    path('auth/token/', get_token, name='get-token'),
]
