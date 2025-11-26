from django.db import models
from tenancy.models.tenant import Tenant

class Wallet(models.Model):
    tenant = models.OneToOneField(
        Tenant, on_delete=models.CASCADE, related_name="wallet"
    )
    balance = models.DecimalField(max_digits=14, decimal_places=5, default=0)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Wallet of {self.tenant.name}: {self.balance}"
