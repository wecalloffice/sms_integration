from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .serializers import (
    WeCallTokenObtainPairSerializer,
    UserSerializer,
    ApiKeyGenerateSerializer,
)


class LoginView(TokenObtainPairView):
    """
    POST /api/v1/auth/login/
    body: { "email": "...", "password": "..." }
    """
    serializer_class = WeCallTokenObtainPairSerializer


class RefreshView(TokenRefreshView):
    """
    POST /api/v1/auth/refresh/
    body: { "refresh": "..." }
    """
    pass


class MeView(generics.RetrieveAPIView):
    """
    GET /api/v1/auth/me/
    Return current authenticated user.
    """
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class GenerateApiKeyView(generics.CreateAPIView):
    """
    POST /api/v1/auth/api-key/
    Returns: { "api_key": "<raw-key>" }
    """
    serializer_class = ApiKeyGenerateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data={})
        serializer.is_valid(raise_exception=True)
        data = serializer.save()
        return Response(data)
