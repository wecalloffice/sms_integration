from django.db import models
from tenancy.models.tenant import Tenant

class SmsDailyStats(models.Model):
    tenant = models.ForeignKey(
        Tenant, on_delete=models.CASCADE, related_name="sms_stats"
    )

    date = models.DateField()
    messages_sent = models.PositiveIntegerField(default=0)
    messages_delivered = models.PositiveIntegerField(default=0)
    messages_failed = models.PositiveIntegerField(default=0)

    total_cost = models.DecimalField(max_digits=12, decimal_places=5, default=0)
    total_revenue = models.DecimalField(max_digits=12, decimal_places=5, default=0)

    class Meta:
        unique_together = ("tenant", "date")

    def __str__(self):
        return f"{self.tenant.name} - {self.date}"
