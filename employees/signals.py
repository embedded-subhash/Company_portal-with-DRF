from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from api.middleware import get_current_request
from audit_logs.services import create_audit_log
from employees.models import Employee


def _request_meta():
    request = get_current_request()
    if not request:
        return None, None

    ip_address = request.META.get("HTTP_X_FORWARDED_FOR")
    if ip_address:
        ip_address = ip_address.split(",")[0].strip()
    else:
        ip_address = request.META.get("REMOTE_ADDR")

    return getattr(request, "user", None), ip_address


@receiver(post_save, sender=Employee)
def log_employee_save(sender, instance, created, **kwargs):
    user, ip_address = _request_meta()
    create_audit_log(
        user=user,
        action="Employee Created" if created else "Employee Updated",
        module="Employee",
        ip_address=ip_address,
    )


@receiver(post_delete, sender=Employee)
def log_employee_delete(sender, instance, **kwargs):
    user, ip_address = _request_meta()
    create_audit_log(
        user=user,
        action="Employee Deleted",
        module="Employee",
        ip_address=ip_address,
    )
