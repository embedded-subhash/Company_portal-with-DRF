from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from .pagination import EmployeePagination
from employees.models import Employee
from departments.models import Department
from accounts.models import User
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .serializers import (
    EmailTokenObtainPairSerializer,
    EmployeeSerializer,
    DepartmentSerializer,
    UserSerializer
)

from .permissions import (
    IsAdminHRManagerOrReadOnly,
    IsAdminOnly
)


class EmailTokenObtainPairView(TokenObtainPairView):
    serializer_class = EmailTokenObtainPairSerializer


class EmployeeViewSet(ModelViewSet):

    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

    pagination_class = EmployeePagination
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
