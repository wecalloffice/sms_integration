from rest_framework import serializers
from tenancy.models import Tenant, TenantDomain
from identity.models import User


class ClientCreateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=200)
    primary_domain = serializers.CharField(
        max_length=255, required=False, allow_blank=True, allow_null=True
    )

    admin_email = serializers.EmailField()
    admin_password = serializers.CharField(write_only=True, min_length=8)

    def validate_name(self, value):
        if Tenant.objects.filter(name__iexact=value).exists():
            raise serializers.ValidationError("A tenant with this name already exists.")
        return value

    def validate_primary_domain(self, value):
        if value and TenantDomain.objects.filter(domain__iexact=value).exists():
            raise serializers.ValidationError("This domain is already in use.")
        return value

    def create(self, validated_data):
        name = validated_data["name"]
        primary_domain = validated_data.get("primary_domain")

        admin_email = validated_data["admin_email"]
        admin_password = validated_data["admin_password"]

        request = self.context["request"]
        reseller_tenant = request.user.tenant

        client_tenant = Tenant.objects.create(
            name=name,
            tenant_type="CLIENT",
            parent=reseller_tenant,
            is_active=True,
        )

        if primary_domain:
            TenantDomain.objects.create(
                tenant=client_tenant,
                domain=primary_domain,
                is_primary=True,
            )

        admin_user = User.objects.create_user(
            email=admin_email,
            password=admin_password,
            tenant=client_tenant,
            role="CLIENT_ADMIN",
            is_staff=False,
        )

        return {
            "tenant_id": client_tenant.id,
            "tenant_name": client_tenant.name,
            "admin_user_id": admin_user.id,
            "admin_email": admin_user.email,
            "parent_reseller": reseller_tenant.name,
        }
