from rest_framework.permissions import BasePermission


class IsAdminHRManagerOrReadOnly(BasePermission):

    def has_permission(self, request, view):

        user = request.user

        if not user or not user.is_authenticated:
            return False

        # Everyone can view
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True

        # Admin: Full access
        role = getattr(user, "role", None)

        if role == 'ADMIN':
            return True

        # HR: Create and Update only
        if role == 'HR':

            if request.method in ['POST', 'PUT', 'PATCH']:
                return True

        # Manager: View only
        if role == 'MANAGER':
            return False

        # Employee: View only
        if role == 'EMPLOYEE':
            return False

        return False


class IsAdminOnly(BasePermission):

    def has_permission(self, request, view):

        user = request.user
        return bool(
            user
            and user.is_authenticated
            and getattr(user, "role", None) == 'ADMIN'
        )
