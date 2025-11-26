from django.utils.deprecation import MiddlewareMixin
from tenancy.models import TenantDomain

class TenantMiddleware(MiddlewareMixin):
    def process_request(self, request):
        host = request.get_host().split(':')[0]  # remove port
        try:
            tenant_domain = TenantDomain.objects.select_related("tenant").get(domain=host)
            request.tenant = tenant_domain.tenant
        except TenantDomain.DoesNotExist:
            request.tenant = None  # or default platform tenant
