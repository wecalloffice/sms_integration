from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsPlatformAdmin(BasePermission):
    """
    Only users with role=PLATFORM_ADMIN.
    Used for System Owner actions (weCall).
    """

    def has_permission(self, request, view):
        user = request.user
        return bool(
            user
            and user.is_authenticated
            and getattr(user, "role", None) == "PLATFORM_ADMIN"
        )


class IsResellerAdmin(BasePermission):
    """
    Only users with role=RESELLER_ADMIN.
    Used for reseller dashboard actions.
    """

    def has_permission(self, request, view):
        user = request.user
        return bool(
            user
            and user.is_authenticated
            and getattr(user, "role", None) == "RESELLER_ADMIN"
        )


class IsClientAdmin(BasePermission):
    """
    Only users with role=CLIENT_ADMIN.
    """

    def has_permission(self, request, view):
        user = request.user
        return bool(
            user
            and user.is_authenticated
            and getattr(user, "role", None) == "CLIENT_ADMIN"
        )
