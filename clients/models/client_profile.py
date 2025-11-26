from django.db import models
from tenancy.models.tenant import Tenant

class ClientProfile(models.Model):
    """
    Additional details about client companies (schools, banks, SACCOs, restaurants).
    """
    tenant = models.OneToOneField(
        Tenant, on_delete=models.CASCADE, related_name="client_profile"
    )

    business_type = models.CharField(
        max_length=100, 
        null=True, 
        blank=True,
        help_text="Eg: School, Bank, SACCO, Retail, NGO"
    )
    industry = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        help_text="Optional industry classification"
    )
    website = models.URLField(null=True, blank=True)

    contact_person = models.CharField(max_length=255, null=True, blank=True)
    contact_email = models.EmailField(null=True, blank=True)
    contact_phone = models.CharField(max_length=50, null=True, blank=True)

    address = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Client Profile: {self.tenant.name}"
