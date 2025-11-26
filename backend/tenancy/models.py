import uuid
from django.db import models

class Tenant(models.Model):
    TENANT_TYPES = (
        ('PLATFORM', 'Platform Owner'),
        ('RESELLER', 'Reseller'),
        ('CLIENT', 'Client'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200, unique=True)
    tenant_type = models.CharField(max_length=20, choices=TENANT_TYPES)
    parent = models.ForeignKey(
        'self', null=True, blank=True, on_delete=models.SET_NULL,
        help_text="For CLIENT tenants under RESELLERS"
    )
    is_active = models.BooleanField(default=True)

    # For SIP/SMS shared wallet in future
    wallet_enabled = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.tenant_type})"


class TenantDomain(models.Model):
    domain = models.CharField(max_length=255, unique=True)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    is_primary = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.domain} -> {self.tenant.name}"


class TenantBranding(models.Model):
    tenant = models.OneToOneField(Tenant, on_delete=models.CASCADE, related_name="branding")

    logo = models.URLField(null=True, blank=True)
    favicon = models.URLField(null=True, blank=True)
    primary_color = models.CharField(max_length=20, default="#0057ff")
    secondary_color = models.CharField(max_length=20, default="#002266")
    dashboard_title = models.CharField(max_length=200, default="WeCallSMS Portal")

    custom_css = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Branding for {self.tenant.name}"
