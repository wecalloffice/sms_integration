# from rest_framework import generics
# from identity.permissions import IsPlatformAdmin
# from tenancy.serializers.reseller_serializers import ResellerCreateSerializer

# from identity.permissions import IsPlatformAdmin, IsResellerAdmin
# from tenancy.serializers.reseller_serializers import ResellerCreateSerializer
# from tenancy.serializers.client_serializers import ClientCreateSerializer

# from tenancy.models import Tenant


# class ResellerCreateView(generics.CreateAPIView):
#     """
#     POST /api/v1/tenants/resellers/
#     Only System Owner (PLATFORM_ADMIN) can call this.
#     """
#     serializer_class = ResellerCreateSerializer
#     permission_classes = [permissions.IsAuthenticated, IsPlatformAdmin]


# class ClientCreateView(generics.CreateAPIView):
#     """
#     POST /api/v1/tenants/clients/
#     Only RESELLER_ADMIN can call this - creates new CLIENT tenant under reseller.
#     """
#     serializer_class = ClientCreateSerializer
#     permission_classes = [permissions.IsAuthenticated, IsResellerAdmin]


# class ResellerListView(generics.ListAPIView):
#     """
#     GET /api/v1/tenants/resellers/
#     Platform admin: list all resellers.
#     """
#     permission_classes = [permissions.IsAuthenticated, IsPlatformAdmin]

#     def list(self, request, *args, **kwargs):
#         resellers = Tenant.objects.filter(tenant_type="RESELLER")
#         data = [
#             {
#                 "id": str(t.id),
#                 "name": t.name,
#                 "parent": t.parent.name if t.parent else None,
#                 "is_active": t.is_active,
#             }
#             for t in resellers
#         ]
#         return Response(data)


# class ClientListView(generics.ListAPIView):
#     """
#     GET /api/v1/tenants/clients/
#     If called by RESELLER_ADMIN -> list their clients.
#     If called by PLATFORM_ADMIN -> list all clients.
#     """
#     permission_classes = [permissions.IsAuthenticated]

#     def list(self, request, *args, **kwargs):
#         user = request.user
#         qs = Tenant.objects.filter(tenant_type="CLIENT")

#         if user.role == "RESELLER_ADMIN":
#             qs = qs.filter(parent=user.tenant)

#         data = [
#             {
#                 "id": str(t.id),
#                 "name": t.name,
#                 "parent_reseller": t.parent.name if t.parent else None,
#                 "is_active": t.is_active,
#             }
#             for t in qs
#         ]
#         return Response(data)
# class ResellerCreateView(generics.CreateAPIView):
#     serializer_class = ResellerCreateSerializer
#     permission_classes = [IsPlatformAdmin]

from rest_framework import generics, permissions
from rest_framework.response import Response

from tenancy.models import Tenant
from tenancy.serializers import ResellerCreateSerializer, ClientCreateSerializer


class IsPlatformAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.role == "PLATFORM_ADMIN"
        )


class IsResellerOrPlatform(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.role in ["PLATFORM_ADMIN", "RESELLER_ADMIN"]
        )


class ResellerCreateView(generics.GenericAPIView):
    """
    System Owner (WeCall) creates a RESELLER like Norrsken.
    """
    serializer_class = ResellerCreateSerializer
    permission_classes = [permissions.IsAuthenticated, IsPlatformAdmin]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = serializer.save()
        return Response(result, status=201)


class ClientCreateView(generics.GenericAPIView):
    """
    Platform or Reseller can create CLIENT (e.g. Liquid or a Norrsken company).
    """
    serializer_class = ClientCreateSerializer
    permission_classes = [permissions.IsAuthenticated, IsResellerOrPlatform]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        result = serializer.save()
        return Response(result, status=201)


class ResellerListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated, IsPlatformAdmin]

    def list(self, request, *args, **kwargs):
        resellers = Tenant.objects.filter(tenant_type="RESELLER")
        data = [
            {
                "id": str(t.id),
                "name": t.name,
                "email": t.company_email,
                "parent": t.parent.name if t.parent else None,
            }
            for t in resellers
        ]
        return Response(data)


class ClientListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request, *args, **kwargs):
        user = request.user
        qs = Tenant.objects.filter(tenant_type="CLIENT")

        if user.role == "RESELLER_ADMIN":
            qs = qs.filter(parent=user.tenant)
        elif user.role == "PLATFORM_ADMIN":
            pass
        else:
            qs = qs.filter(id=user.tenant.id)

        data = [
            {
                "id": str(t.id),
                "name": t.name,
                "email": t.company_email,
                "parent": t.parent.name if t.parent else None,
            }
            for t in qs
        ]
        return Response(data)
