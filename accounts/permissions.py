"""
Role-based and object-level permission classes.

Role checks are done against request.user.role rather than Django's
groups/permissions system, matching the four-role model (Admin, HR,
Manager, Employee) from the module spec. Every denial is written to
the SecurityLog so unauthorized-access attempts are auditable.
"""
from rest_framework.permissions import BasePermission, SAFE_METHODS

from .security import log_event
from logs.models import SecurityLog


class _RoleBasePermission(BasePermission):
    allowed_roles = ()
    message = "You do not have permission to perform this action."

    def has_permission(self, request, view):
        allowed = bool(
            request.user
            and request.user.is_authenticated
            and request.user.role in self.allowed_roles
        )
        if not allowed:
            log_event(
                request,
                SecurityLog.Action.PERMISSION_DENIED,
                SecurityLog.Status.FAILURE,
                user=getattr(request, "user", None),
                detail=f"Required role in {self.allowed_roles}, got "
                       f"'{getattr(getattr(request, 'user', None), 'role', 'anonymous')}'",
            )
        return allowed


class IsAdmin(_RoleBasePermission):
    allowed_roles = ("ADMIN",)


class IsHR(_RoleBasePermission):
    allowed_roles = ("ADMIN", "HR")


class IsManager(_RoleBasePermission):
    allowed_roles = ("ADMIN", "MANAGER")


class IsEmployee(_RoleBasePermission):
    """Any authenticated platform user (all four roles)."""
    allowed_roles = ("ADMIN", "HR", "MANAGER", "EMPLOYEE")


class IsAdminOrHRorManager(_RoleBasePermission):
    """Used for dashboard APIs: Admin, HR, and Manager -- not plain Employee."""
    allowed_roles = ("ADMIN", "HR", "MANAGER")


class IsEmployeeReadOnlySelf(BasePermission):
    """
    Object-level permission for the employee profile endpoint.

    - Admin/HR/Manager can read or write any employee record.
    - A plain Employee may only GET (read-only) their own record; any
      access to another employee's object is denied and logged.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        user = request.user
        if user.role in ("ADMIN", "HR", "MANAGER"):
            return True

        owns_record = getattr(obj, "user_id", None) == user.id
        if not owns_record:
            log_event(
                request,
                SecurityLog.Action.UNAUTHORIZED_ACCESS,
                SecurityLog.Status.FAILURE,
                user=user,
                detail=f"Employee {user.id} attempted to access profile of object {obj.pk}",
            )
            return False

        if request.method not in SAFE_METHODS:
            log_event(
                request,
                SecurityLog.Action.PERMISSION_DENIED,
                SecurityLog.Status.FAILURE,
                user=user,
                detail="Employee attempted to modify own profile via restricted endpoint",
            )
            return False

        return True
