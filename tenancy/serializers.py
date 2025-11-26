from rest_framework import serializers
from tenancy.models import Tenant
from identity.models import User


class ResellerCreateSerializer(serializers.Serializer):
    # Company fields
    name = serializers.CharField(max_length=200)
    legal_name = serializers.CharField(max_length=255, required=False, allow_blank=True)
    company_email = serializers.EmailField(required=False, allow_blank=True)
    company_phone = serializers.CharField(max_length=50, required=False, allow_blank=True)
    website = serializers.URLField(required=False, allow_blank=True)

    country = serializers.CharField(max_length=100, required=False, allow_blank=True)
    city = serializers.CharField(max_length=100, required=False, allow_blank=True)
    address = serializers.CharField(max_length=255, required=False, allow_blank=True)

    logo_url = serializers.URLField(required=False, allow_blank=True)
    primary_color = serializers.CharField(max_length=20, required=False, default="#0057ff")
    secondary_color = serializers.CharField(max_length=20, required=False, default="#002266")

    domain = serializers.CharField(max_length=255, required=False, allow_blank=True)

    # Admin user fields
    admin_email = serializers.EmailField()
    admin_password = serializers.CharField(write_only=True)
    admin_first_name = serializers.CharField(max_length=100)
    admin_last_name = serializers.CharField(max_length=100)

    def create(self, validated_data):
        # 1. Get platform tenant (WeCall)
        platform_tenant = Tenant.objects.filter(tenant_type="PLATFORM").first()
        if not platform_tenant:
            platform_tenant = Tenant.objects.create(
                tenant_type="PLATFORM",
                name="WeCall",
                legal_name="WeCall Ltd",
            )

        # Extract user data
        admin_email = validated_data.pop("admin_email")
        admin_password = validated_data.pop("admin_password")
        admin_first_name = validated_data.pop("admin_first_name")
        admin_last_name = validated_data.pop("admin_last_name")

        # 2. Create reseller tenant
        reseller = Tenant.objects.create(
            tenant_type="RESELLER",
            parent=platform_tenant,
            **validated_data,
        )

        # 3. Create reseller admin user
        admin_user = User.objects.create_user(
            email=admin_email,
            password=admin_password,
            tenant=reseller,
            role="RESELLER_ADMIN",
            first_name=admin_first_name,
            last_name=admin_last_name,
            is_staff=True,
        )

        return {
            "tenant_id": reseller.id,
            "tenant_name": reseller.name,
            "admin_email": admin_user.email,
        }


class ClientCreateSerializer(serializers.Serializer):
    # Company fields
    name = serializers.CharField(max_length=200)
    legal_name = serializers.CharField(max_length=255, required=False, allow_blank=True)
    company_email = serializers.EmailField(required=False, allow_blank=True)
    company_phone = serializers.CharField(max_length=50, required=False, allow_blank=True)
    website = serializers.URLField(required=False, allow_blank=True)

    country = serializers.CharField(max_length=100, required=False, allow_blank=True)
    city = serializers.CharField(max_length=100, required=False, allow_blank=True)
    address = serializers.CharField(max_length=255, required=False, allow_blank=True)

    logo_url = serializers.URLField(required=False, allow_blank=True)
    primary_color = serializers.CharField(max_length=20, required=False, default="#0057ff")
    secondary_color = serializers.CharField(max_length=20, required=False, default="#002266")

    domain = serializers.CharField(max_length=255, required=False, allow_blank=True)

    # Admin user fields
    admin_email = serializers.EmailField()
    admin_password = serializers.CharField(write_only=True)
    admin_first_name = serializers.CharField(max_length=100)
    admin_last_name = serializers.CharField(max_length=100)

    def create(self, validated_data):
        request = self.context["request"]
        user = request.user

        # parent tenant = current user's tenant (reseller or platform)
        parent_tenant = user.tenant

        # Extract user data
        admin_email = validated_data.pop("admin_email")
        admin_password = validated_data.pop("admin_password")
        admin_first_name = validated_data.pop("admin_first_name")
        admin_last_name = validated_data.pop("admin_last_name")

        # Tenant type is always CLIENT here
        client_tenant = Tenant.objects.create(
            tenant_type="CLIENT",
            parent=parent_tenant,
            **validated_data,
        )

        admin_user = User.objects.create_user(
            email=admin_email,
            password=admin_password,
            tenant=client_tenant,
            role="CLIENT_ADMIN",
            first_name=admin_first_name,
            last_name=admin_last_name,
        )

        return {
            "tenant_id": client_tenant.id,
            "tenant_name": client_tenant.name,
            "parent": parent_tenant.name,
            "admin_email": admin_user.email,
        }
