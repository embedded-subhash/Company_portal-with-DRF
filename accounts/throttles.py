"""
Per-endpoint throttle classes (Module 7). Rates are also declared in
settings.DEFAULT_THROTTLE_RATES so they can be tuned without code
changes; the classes here just point DRF at the right rate key and,
for auth attempts, scope by IP rather than user (since the user often
isn't authenticated yet at login).
"""
from rest_framework.throttling import ScopedRateThrottle, SimpleRateThrottle


class AuthRateThrottle(SimpleRateThrottle):
    """5 requests/minute per IP on login/refresh/password endpoints."""
    scope = "auth"

    def get_cache_key(self, request, view):
        ident = self.get_ident(request)
        return self.cache_format % {"scope": self.scope, "ident": ident}


class EmployeeRateThrottle(ScopedRateThrottle):
    """100 requests/minute, scoped per authenticated user."""
    scope = "employee"


class ReportRateThrottle(ScopedRateThrottle):
    """20 requests/minute, scoped per authenticated user."""
    scope = "report"
