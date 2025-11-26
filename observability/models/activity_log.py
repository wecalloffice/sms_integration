from django.db import models
from identity.models.user import User
from tenancy.models.tenant import Tenant

class ActivityLog(models.Model):

    ACTIONS = (
        ("LOGIN", "Login"),
        ("LOGOUT", "Logout"),
        ("CREATE_CLIENT", "Client created"),
        ("CREATE_USER", "User created"),
        ("WALLET_TOPUP", "Wallet Top-up"),
        ("PRICE_UPDATE", "Pricing change"),
        ("SEND_SMS", "SMS sent"),
        ("UPDATE_SETTINGS", "Settings changed"),
    )

    tenant = models.ForeignKey(
        Tenant, on_delete=models.CASCADE, related_name="activities"
    )

    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True
    )

    action_type = models.CharField(max_length=50, choices=ACTIONS)
    message = models.TextField(null=True, blank=True)
    metadata = models.JSONField(default=dict, blank=True)

    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.action_type} by {self.user} at {self.timestamp}"
