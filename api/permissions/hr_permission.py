from rest_framework.permissions import SAFE_METHODS, BasePermission

from .admin_permission import _role


class IsHR(BasePermission):
    """
    HR can Create and Update, but cannot Delete.
    (Admin is always allowed too, since Admin has full access.)
    """

    message = "HR users cannot perform this action (e.g. delete)."

    def has_permission(self, request, view):
        role = _role(request)
        if role == "admin":
            return True
        if role != "hr":
            return False
        if request.method == "DELETE":
            return False
        # SAFE_METHODS (GET/HEAD/OPTIONS), POST, PUT, PATCH are allowed for HR.
        return True

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)
