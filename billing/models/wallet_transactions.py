import uuid
from django.db import models
from tenancy.models.tenant import Tenant

class WalletTransaction(models.Model):
    TRANSACTION_TYPES = (
        ("TOPUP", "Top-up"),
        ("DEBIT", "Debit"),
        ("ADJUST", "Adjustment"),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tenant = models.ForeignKey(
        Tenant, on_delete=models.CASCADE, related_name="wallet_transactions"
    )

    txn_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=14, decimal_places=5)
    balance_after = models.DecimalField(max_digits=14, decimal_places=5)

    description = models.TextField(null=True, blank=True)
    metadata = models.JSONField(default=dict, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.tenant.name} - {self.txn_type} - {self.amount}"
