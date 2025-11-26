from django.urls import path
from identity.views import LoginView, RefreshView, MeView, GenerateApiKeyView

urlpatterns = [
    path("auth/login/", LoginView.as_view(), name="auth-login"),
    path("auth/refresh/", RefreshView.as_view(), name="auth-refresh"),
    path("auth/me/", MeView.as_view(), name="auth-me"),
    path("auth/api-key/", GenerateApiKeyView.as_view(), name="auth-api-key"),
]
