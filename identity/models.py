import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

from tenancy.models import Tenant


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, tenant=None, role="CLIENT_USER", **extra_fields):
        if not email:
            raise ValueError("Users must have an email address")

        if tenant is None:
            raise ValueError("User must belong to a tenant")

        email = self.normalize_email(email)
        user = self.model(email=email, tenant=tenant, role=role, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create a superuser for the PLATFORM tenant.
        If PLATFORM tenant doesn't exist, create one named 'WeCall'.
        """
        platform_tenant, _ = Tenant.objects.get_or_create(
            tenant_type="PLATFORM",
            name="WeCall",
            defaults={"legal_name": "WeCall Ltd"},
        )

        extra_fields.setdefault("role", "PLATFORM_ADMIN")
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(email, password, tenant=platform_tenant, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (
        ("PLATFORM_ADMIN", "Platform Admin"),
        ("RESELLER_ADMIN", "Reseller Admin"),
        ("RESELLER_USER", "Reseller User"),
        ("CLIENT_ADMIN", "Client Admin"),
        ("CLIENT_USER", "Client User"),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Link to tenant (WeCall, Norrsken, Liquid, etc.)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name="users")

    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)

    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return f"{self.email} ({self.role})"
