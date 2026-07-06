from rest_framework.permissions import SAFE_METHODS, BasePermission

from .admin_permission import _role


class IsEmployeeReadOnlySelf(BasePermission):
    """
    Employee can only VIEW their own profile. No create/update/delete,
    and no access to other employees' records.
    """

    message = "Employees may only view their own profile."

    def has_permission(self, request, view):
        role = _role(request)
        if role in ("admin", "hr"):
            return True
        if role != "employee":
            return False
        return request.method in SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        role = _role(request)
        if role in ("admin", "hr"):
            return True
        if role != "employee" or request.method not in SAFE_METHODS:
            return False
        return getattr(obj, "user_id", None) == request.user.id
