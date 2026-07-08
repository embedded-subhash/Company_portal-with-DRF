from .models import AuditLog


def create_audit_log(user=None, action="", module="", ip_address=None):
    return AuditLog.objects.create(
        user=user if getattr(user, "is_authenticated", False) else None,
        action=action,
        module=module,
        ip_address=ip_address,
    )
