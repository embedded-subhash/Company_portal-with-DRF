from rest_framework.permissions import BasePermission


class IsAdminHRManagerOrReadOnly(BasePermission):

    def has_permission(self, request, view):

        user = request.user

        # Everyone can view
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True

        # Admin: Full access
        if user.role == 'ADMIN':
            return True

        # HR: Create and Update only
        if user.role == 'HR':

            if request.method in ['POST', 'PUT', 'PATCH']:
                return True

        # Manager: View only
        if user.role == 'MANAGER':
            return False

        # Employee: View only
        if user.role == 'EMPLOYEE':
            return False

        return False


class IsAdminOnly(BasePermission):

    def has_permission(self, request, view):

        return request.user.role == 'ADMIN'