# import uuid
# from django.db import models


# class Tenant(models.Model):
#     TENANT_TYPES = (
#         ("PLATFORM", "Platform Owner"),
#         ("RESELLER", "Reseller"),
#         ("CLIENT", "Client"),
#     )

#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

#     # Type & hierarchy
#     tenant_type = models.CharField(max_length=20, choices=TENANT_TYPES)
#     parent = models.ForeignKey(
#         "self",
#         null=True,
#         blank=True,
#         on_delete=models.SET_NULL,
#         related_name="children",
#         help_text="For a CLIENT, parent is Reseller or Platform. For RESELLER, parent is Platform.",
#     )

#     # Basic company info
#     name = models.CharField(max_length=200, unique=True)
#     legal_name = models.CharField(max_length=255, blank=True)
#     company_email = models.EmailField(blank=True)
#     company_phone = models.CharField(max_length=50, blank=True)
#     website = models.URLField(blank=True)

#     country = models.CharField(max_length=100, blank=True)
#     city = models.CharField(max_length=100, blank=True)
#     address = models.CharField(max_length=255, blank=True)

#     # Basic branding
#     logo_url = models.URLField(blank=True)
#     primary_color = models.CharField(max_length=20, default="#0057ff")
#     secondary_color = models.CharField(max_length=20, default="#002266")

#     # Portal domain (optional for now)
#     domain = models.CharField(max_length=255, blank=True)

#     is_active = models.BooleanField(default=True)
#     created_at = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         ordering = ["tenant_type", "name"]

#     def __str__(self):
#         return f"{self.name} ({self.tenant_type})"
import uuid
from django.db import models


class Tenant(models.Model):
    TENANT_TYPES = (
        ("PLATFORM", "Platform Owner"),
        ("RESELLER", "Reseller"),
        ("CLIENT", "Client"),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    tenant_type = models.CharField(max_length=20, choices=TENANT_TYPES)
    parent = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="children",
    )

    name = models.CharField(max_length=200, unique=True)
    legal_name = models.CharField(max_length=255, blank=True)
    company_email = models.EmailField(blank=True)
    company_phone = models.CharField(max_length=50, blank=True)
    website = models.URLField(blank=True)
    country = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    address = models.CharField(max_length=255, blank=True)

    logo_url = models.URLField(blank=True)
    primary_color = models.CharField(max_length=20, default="#0057ff")
    secondary_color = models.CharField(max_length=20, default="#002266")

    domain = models.CharField(max_length=255, blank=True)

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["tenant_type", "name"]

    def __str__(self):
        return f"{self.name} ({self.tenant_type})"


class TenantDomain(models.Model):
    tenant = models.ForeignKey(
        Tenant,
        on_delete=models.CASCADE,
        related_name="domains",
    )
    domain = models.CharField(max_length=255, unique=True)
    is_primary = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.domain} → {self.tenant.name}"
