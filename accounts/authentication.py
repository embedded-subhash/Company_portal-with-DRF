"""
Thin wrapper around SimpleJWT's JWTAuthentication that logs failed
authentication attempts (e.g. expired/blacklisted/malformed tokens)
to the SecurityLog, so unauthorized-access attempts on protected
endpoints are auditable even before a permission class runs.
"""
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, AuthenticationFailed

from .security import log_event
from logs.models import SecurityLog


class LoggingJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        try:
            result = super().authenticate(request)
        except (InvalidToken, AuthenticationFailed) as exc:
            auth_header = request.META.get("HTTP_AUTHORIZATION", "")
            if auth_header:
                log_event(
                    request,
                    SecurityLog.Action.UNAUTHORIZED_ACCESS,
                    SecurityLog.Status.FAILURE,
                    detail=f"Invalid/expired token on {request.path}: {exc}",
                )
            raise
        return result
