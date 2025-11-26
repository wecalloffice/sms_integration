from rest_framework import generics, permissions
from rest_framework.response import Response

from identity.permissions import IsPlatformAdmin, IsResellerAdmin
from tenancy.serializers.reseller_serializers import ResellerCreateSerializer
from tenancy.serializers.client_serializers import ClientCreateSerializer

from tenancy.models import Tenant


class ResellerCreateView(generics.CreateAPIView):
    """
    POST /api/v1/tenants/resellers/
    Only System Owner (PLATFORM_ADMIN) can call this.
    """
    serializer_class = ResellerCreateSerializer
    permission_classes = [permissions.IsAuthenticated, IsPlatformAdmin]


class ClientCreateView(generics.CreateAPIView):
    """
    POST /api/v1/tenants/clients/
    Only RESELLER_ADMIN can call this - creates new CLIENT tenant under reseller.
    """
    serializer_class = ClientCreateSerializer
    permission_classes = [permissions.IsAuthenticated, IsResellerAdmin]


class ResellerListView(generics.ListAPIView):
    """
    GET /api/v1/tenants/resellers/
    Platform admin: list all resellers.
    """
    permission_classes = [permissions.IsAuthenticated, IsPlatformAdmin]

    def list(self, request, *args, **kwargs):
        resellers = Tenant.objects.filter(tenant_type="RESELLER")
        data = [
            {
                "id": str(t.id),
                "name": t.name,
                "parent": t.parent.name if t.parent else None,
                "is_active": t.is_active,
            }
            for t in resellers
        ]
        return Response(data)


class ClientListView(generics.ListAPIView):
    """
    GET /api/v1/tenants/clients/
    If called by RESELLER_ADMIN -> list their clients.
    If called by PLATFORM_ADMIN -> list all clients.
    """
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request, *args, **kwargs):
        user = request.user
        qs = Tenant.objects.filter(tenant_type="CLIENT")

        if user.role == "RESELLER_ADMIN":
            qs = qs.filter(parent=user.tenant)

        data = [
            {
                "id": str(t.id),
                "name": t.name,
                "parent_reseller": t.parent.name if t.parent else None,
                "is_active": t.is_active,
            }
            for t in qs
        ]
        return Response(data)
