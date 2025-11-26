from rest_framework import authentication, exceptions
from .models import User


class ApiKeyAuthentication(authentication.BaseAuthentication):
    """
    Allows requests authenticated with X-API-Key header or ?api_key=.
    Used for server-to-server SMS API calls.
    """

    keyword = "X-API-Key"

    def authenticate(self, request):
        # 1) Header
        api_key = request.headers.get(self.keyword)

        # 2) Fallback to query param
        if not api_key:
            api_key = request.query_params.get("api_key")

        if not api_key:
            return None  # no API key means "try other auths"

        try:
            # We can't search by api_key_hash directly, so we check each candidate
            # Better: store API keys in separate table; for now, loop with filter.
            users = User.objects.filter(is_active=True, api_key_hash__isnull=False)
            for user in users:
                if user.check_api_key(api_key):
                    return (user, None)
        except Exception:
            raise exceptions.AuthenticationFailed("Invalid API key")

        raise exceptions.AuthenticationFailed("Invalid API key")
