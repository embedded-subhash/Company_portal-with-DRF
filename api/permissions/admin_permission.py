from rest_framework.permissions import BasePermission


def _role(request):
    user = request.user
    if not user or not user.is_authenticated:
        return None
    if user.is_superuser:
        return "admin"
    profile = getattr(user, "profile", None)
    return profile.role if profile else None


class IsAdmin(BasePermission):
    """
    Admin can Create, Update, Delete (full access).
    """

    message = "Only Admin users can perform this action."

    def has_permission(self, request, view):
        return _role(request) == "admin"

    def has_object_permission(self, request, view, obj):
        return _role(request) == "admin"
