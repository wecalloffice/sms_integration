from rest_framework import generics, permissions
from rest_framework.response import Response

from identity.serializers import LoginSerializer
from tenancy.serializers import ResellerCreateSerializer, ClientCreateSerializer
from tenancy.models import Tenant


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]

        return Response({
            "user": {
                "id": str(user.id),
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "role": user.role,
            },
            "tenant": {
                "id": str(user.tenant.id),
                "name": user.tenant.name,
                "type": user.tenant.tenant_type,
            },
        })
