"""
Custom permissions package (Module 3).

Exposes:
    IsAdmin                  - admin_permission.py
    IsHR                     - hr_permission.py
    IsEmployeeReadOnlySelf   - employee_permission.py
    EmployeeAccessPolicy     - combined policy used by EmployeeViewSet
"""

from rest_framework.permissions import BasePermission, SAFE_METHODS

from .admin_permission import IsAdmin, _role
from .hr_permission import IsHR
from .employee_permission import IsEmployeeReadOnlySelf

__all__ = ["IsAdmin", "IsHR", "IsEmployeeReadOnlySelf", "EmployeeAccessPolicy"]


class EmployeeAccessPolicy(BasePermission):
    """
    Single combined policy for the Employee resource:

        Admin    -> create, update, delete (full access)
        HR       -> create, update (cannot delete)
        Employee -> view own profile only
    """

    def has_permission(self, request, view):
        role = _role(request)
        if role == "admin":
            return True
        if role == "hr":
            return request.method != "DELETE"
        if role == "employee":
            return request.method in SAFE_METHODS
        return False

    def has_object_permission(self, request, view, obj):
        role = _role(request)
        if role == "admin":
            return True
        if role == "hr":
            return request.method != "DELETE"
        if role == "employee":
            return request.method in SAFE_METHODS and getattr(obj, "user_id", None) == request.user.id
        return False
