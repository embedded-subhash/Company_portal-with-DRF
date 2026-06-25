from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from employees.models import Employee
from departments.models import Department
from accounts.models import User

from .serializers import (
    EmployeeSerializer,
    DepartmentSerializer,
    UserSerializer
)

from .permissions import (
    IsAdminHRManagerOrReadOnly,
    IsAdminOnly
)


class EmployeeViewSet(ModelViewSet):

    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [
        IsAuthenticated,
        IsAdminHRManagerOrReadOnly
    ]


class DepartmentViewSet(ModelViewSet):

    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [
        IsAuthenticated,
        IsAdminOnly
    ]


class UserViewSet(ModelViewSet):

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [
        IsAuthenticated,
        IsAdminOnly
    ]