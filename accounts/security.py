"""
Central helper for writing to the SecurityLog audit trail and for
extracting request metadata (client IP, user agent) consistently
across the accounts app.

Keeping this in one place means every view logs events the same way
instead of each view re-implementing IP extraction / log creation.
"""
from logs.models import SecurityLog


def get_client_ip(request):
    forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if forwarded_for:
        # First entry in the chain is the original client.
        return forwarded_for.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR")


def get_user_agent(request):
    return request.META.get("HTTP_USER_AGENT", "")[:512]


def log_event(request, action, status, user=None, actor_identifier="", detail=""):
    """
    Write a single SecurityLog row. Never raises -- a logging failure
    must not break the request it's trying to audit.
    """
    try:
        SecurityLog.objects.create(
            user=user if (user is not None and getattr(user, "is_authenticated", False)) else None,
            actor_identifier=actor_identifier or (str(user) if user else ""),
            ip_address=get_client_ip(request),
            user_agent=get_user_agent(request),
            action=action,
            status=status,
            path=request.path,
            detail=detail[:512],
        )
    except Exception:
        # Deliberately swallow -- audit logging is best-effort.
        pass
