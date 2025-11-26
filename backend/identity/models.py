import uuid
import secrets
import hashlib
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from tenancy.models import Tenant


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, tenant=None, **extra_fields):
        if not email:
            raise ValueError("Users must have an email")

        email = self.normalize_email(email)

        if tenant is None:
            raise ValueError("User must belong to a tenant")

        user = self.model(email=email, tenant=tenant, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password, **extra_fields):
        tenant, _ = Tenant.objects.get_or_create(
            tenant_type="PLATFORM",
            defaults={"name": "Platform"}
        )

        extra_fields.setdefault("role", "PLATFORM_ADMIN")
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(email, password, tenant=tenant, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (
        ('PLATFORM_ADMIN', 'Platform Admin'),
        ('RESELLER_ADMIN', 'Reseller Admin'),
        ('CLIENT_ADMIN', 'Client Admin'),
        ('CLIENT_USER', 'Client User'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)

    email = models.EmailField(unique=True)
    role = models.CharField(max_length=30, choices=ROLE_CHOICES)

    api_key_hash = models.CharField(max_length=255, null=True, blank=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email

    # --- API KEY SUPPORT ---
    def generate_api_key(self) -> str:
        """Generate a new API key and store its hash."""
        key = secrets.token_urlsafe(32)  # long, high-entropy string
        self.api_key_hash = self._hash_key(key)
        self.save(update_fields=["api_key_hash"])
        return key

    @staticmethod
    def _hash_key(raw_key: str) -> str:
        return hashlib.sha256(raw_key.encode("utf-8")).hexdigest()

    def check_api_key(self, raw_key: str) -> bool:
        if not self.api_key_hash:
            return False
        return self.api_key_hash == self._hash_key(raw_key)
