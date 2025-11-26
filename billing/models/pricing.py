from django.db import models
from tenancy.models.tenant import Tenant

class Pricing(models.Model):
    tenant = models.ForeignKey(
        Tenant, on_delete=models.CASCADE, related_name="pricing"
    )

    country = models.CharField(max_length=100)
    operator = models.CharField(max_length=100)
    sms_type = models.CharField(max_length=50, default="standard")

    cost_price = models.DecimalField(max_digits=10, decimal_places=5)    # what reseller pays
    sell_price = models.DecimalField(max_digits=10, decimal_places=5)    # what client pays

    class Meta:
        unique_together = ("tenant", "country", "operator", "sms_type")

    def __str__(self):
        return f"{self.tenant.name} - {self.country} - {self.operator}"
