# from django.urls import path
# from identity.views import LoginView, RefreshView, MeView, GenerateApiKeyView

# urlpatterns = [
#     path("auth/login/", LoginView.as_view(), name="auth-login"),
#     path("auth/refresh/", RefreshView.as_view(), name="auth-refresh"),
#     path("auth/me/", MeView.as_view(), name="auth-me"),
#     path("auth/api-key/", GenerateApiKeyView.as_view(), name="auth-api-key"),
# ]

from django.urls import path
from identity.views import LoginView, RefreshView, MeView, GenerateApiKeyView
from tenancy.views import (
    ResellerCreateView,
    ClientCreateView,
    ResellerListView,
    ClientListView,
)

urlpatterns = [
    # Auth
    path("auth/login/", LoginView.as_view(), name="auth-login"),
    path("auth/refresh/", RefreshView.as_view(), name="auth-refresh"),
    path("auth/me/", MeView.as_view(), name="auth-me"),
    path("auth/api-key/", GenerateApiKeyView.as_view(), name="auth-api-key"),

    # Tenants (multi-tenant hierarchy)
    # System Owner (weCall) creates resellers
    path("tenants/resellers/", ResellerCreateView.as_view(), name="tenant-reseller-create"),
    path("tenants/resellers/list/", ResellerListView.as_view(), name="tenant-reseller-list"),

    # Reseller creates client tenants
    path("tenants/clients/", ClientCreateView.as_view(), name="tenant-client-create"),
    path("tenants/clients/list/", ClientListView.as_view(), name="tenant-client-list"),
]
