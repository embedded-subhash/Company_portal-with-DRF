from django.db.models.signals import (
    post_save,
    pre_save,
    pre_delete
)

from django.contrib.auth.signals import (
    user_logged_in,
    user_logged_out
)

from django.dispatch import receiver

from employees.models import (
    Employee,
    EmployeeProfile,
    ArchivedEmployee
)

from audit_logs.models import AuditLog


# -------------------------
# CREATE EMPLOYEE PROFILE + AUDIT
# -------------------------
@receiver(post_save, sender=Employee)
def create_employee_profile(sender, instance, created, **kwargs):

    if created:

        EmployeeProfile.objects.create(employee=instance)

        AuditLog.objects.create(
            action='CREATE',
            module='Employee',
            object_id=instance.id
        )

        print(f"Profile created for {instance.employee_id}")


# -------------------------
# TRACK PREVIOUS VALUES
# -------------------------
@receiver(pre_save, sender=Employee)
def track_employee_changes(sender, instance, **kwargs):

    if instance.pk:

        try:
            old = Employee.objects.get(pk=instance.pk)

            if old.salary != instance.salary:
                print(f"Salary changed: {old.salary} -> {instance.salary}")

            if old.department != instance.department:
                print(f"Department changed: {old.department} -> {instance.department}")

        except Employee.DoesNotExist:
            pass


# -------------------------
# ARCHIVE BEFORE DELETE
# -------------------------
@receiver(pre_delete, sender=Employee)
def archive_employee(sender, instance, **kwargs):

    ArchivedEmployee.objects.create(
        employee_id=instance.employee_id,
        first_name=instance.first_name,
        last_name=instance.last_name,
        email=instance.email,
        department_name=str(instance.department),
        salary=instance.salary
    )

    print(f"Archived {instance.employee_id}")


# -------------------------
# LOG DELETE
# -------------------------
@receiver(pre_delete, sender=Employee)
def log_employee_delete(sender, instance, **kwargs):

    AuditLog.objects.create(
        action="DELETE",
        module="Employee",
        object_id=instance.id
    )

    print(f"Deleted {instance.employee_id}")


# -------------------------
# LOGIN AUDIT
# -------------------------
@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):

    AuditLog.objects.create(
        user=user,
        action="LOGIN",
        module="Authentication",
        object_id=user.id,
        ip_address=getattr(request, "META", {}).get("REMOTE_ADDR"),
        request_method=request.method
    )

    print(f"{user.username} logged in")


# -------------------------
# LOGOUT AUDIT
# -------------------------
@receiver(user_logged_out)
def log_user_logout(sender, request, user, **kwargs):

    if user:

        AuditLog.objects.create(
            user=user,
            action="LOGOUT",
            module="Authentication",
            object_id=user.id,
            ip_address=getattr(request, "META", {}).get("REMOTE_ADDR"),
            request_method=request.method
        )

        print(f"{user.username} logged out")