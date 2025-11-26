from rest_framework import serializers
from tenancy.models import Tenant, TenantBranding, TenantDomain
from identity.models import User


class ResellerCreateSerializer(serializers.Serializer):
    # reseller tenant info
    name = serializers.CharField(max_length=200)
    primary_domain = serializers.CharField(max_length=255)

    # branding
    logo = serializers.URLField(required=False, allow_null=True, allow_blank=True)
    favicon = serializers.URLField(required=False, allow_null=True, allow_blank=True)
    primary_color = serializers.CharField(max_length=20, default="#0057ff")
    secondary_color = serializers.CharField(max_length=20, default="#002266")

    # admin user info
    admin_email = serializers.EmailField()
    admin_password = serializers.CharField(write_only=True, min_length=8)

    def validate_name(self, value):
        if Tenant.objects.filter(name__iexact=value).exists():
            raise serializers.ValidationError("A tenant with this name already exists.")
        return value

    def validate_primary_domain(self, value):
        if TenantDomain.objects.filter(domain__iexact=value).exists():
            raise serializers.ValidationError("This domain is already in use.")
        return value

    def create(self, validated_data):
        from tenancy.models import Tenant

        name = validated_data["name"]
        primary_domain = validated_data["primary_domain"]
        logo = validated_data.get("logo")
        favicon = validated_data.get("favicon")
        primary_color = validated_data.get("primary_color", "#0057ff")
        secondary_color = validated_data.get("secondary_color", "#002266")

        admin_email = validated_data["admin_email"]
        admin_password = validated_data["admin_password"]

        # Parent tenant is the platform (owner)
        platform_tenant = Tenant.objects.filter(tenant_type="PLATFORM").first()

        # 1) Create reseller tenant
        reseller_tenant = Tenant.objects.create(
            name=name,
            tenant_type="RESELLER",
            parent=platform_tenant,
            is_active=True,
        )

        # 2) Branding
        TenantBranding.objects.create(
            tenant=reseller_tenant,
            logo=logo,
            favicon=favicon,
            primary_color=primary_color,
            secondary_color=secondary_color,
            dashboard_title=f"{name} SMS Portal",
        )

        # 3) Domain
        TenantDomain.objects.create(
            tenant=reseller_tenant,
            domain=primary_domain,
            is_primary=True,
        )

        # 4) Reseller admin user
        admin_user = User.objects.create_user(
            email=admin_email,
            password=admin_password,
            tenant=reseller_tenant,
            role="RESELLER_ADMIN",
            is_staff=True,
        )

        return {
            "tenant_id": reseller_tenant.id,
            "tenant_name": reseller_tenant.name,
            "admin_user_id": admin_user.id,
            "admin_email": admin_user.email,
            "domain": primary_domain,
        }
