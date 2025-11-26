from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import User


class UserSerializer(serializers.ModelSerializer):
    tenant_name = serializers.CharField(source="tenant.name", read_only=True)
    tenant_type = serializers.CharField(source="tenant.tenant_type", read_only=True)

    class Meta:
        model = User
        fields = ("id", "email", "role", "tenant_name", "tenant_type")


class WeCallTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Custom JWT serializer: includes user & tenant info in token response.
    """

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims
        token["role"] = user.role
        token["tenant_id"] = str(user.tenant_id)
        token["tenant_type"] = user.tenant.tenant_type
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user

        data["user"] = UserSerializer(user).data

        # Add panel redirect suggestion
        if user.role == "PLATFORM_ADMIN":
            data["dashboard"] = "/admin/dashboard"
        elif user.role.startswith("RESELLER"):
            data["dashboard"] = "/reseller/dashboard"
        else:
            data["dashboard"] = "/client/dashboard"

        return data


class ApiKeyGenerateSerializer(serializers.Serializer):
    api_key = serializers.CharField(read_only=True)

    def create(self, validated_data):
        user = self.context["request"].user
        key = user.generate_api_key()
        return {"api_key": key}
