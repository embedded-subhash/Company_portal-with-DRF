from rest_framework.permissions import BasePermission, SAFE_METHODS


def _in_group(user, group_name):
    return user.is_authenticated and (user.is_superuser or user.groups.filter(name=group_name).exists())


class IsAdmin(BasePermission):
    """Full access - Admin group or superuser."""

    def has_permission(self, request, view):
        return bool(request.user and (request.user.is_superuser or _in_group(request.user, "Admin")))


class IsHR(BasePermission):
    """HR group - can manage employees, documents, imports/exports, reports."""

    def has_permission(self, request, view):
        return bool(request.user and (request.user.is_superuser or _in_group(request.user, "HR")))


class IsAdminOrHR(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user
            and (request.user.is_superuser or _in_group(request.user, "Admin") or _in_group(request.user, "HR"))
        )


class IsEmployeeReadOnlySelf(BasePermission):
    """
    Employees can only read/act on their own record. Write access to fields
    outside self-service (e.g. salary) is blocked at the serializer/view layer.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser or _in_group(request.user, "Admin") or _in_group(request.user, "HR"):
            return True
        employee = getattr(obj, "employee", obj)
        return getattr(employee, "user_id", None) == request.user.id
