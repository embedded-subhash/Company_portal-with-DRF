from .auth import EmailTokenObtainPairView, LogoutView, RefreshTokenView
from .departments import DepartmentViewSet
from .employees import EmployeeV1ViewSet, EmployeeV2ViewSet
from .users import UserViewSet

EmployeeViewSet = EmployeeV1ViewSet

__all__ = [
    "DepartmentViewSet",
    "EmailTokenObtainPairView",
    "EmployeeViewSet",
    "EmployeeV1ViewSet",
    "EmployeeV2ViewSet",
    "LogoutView",
    "RefreshTokenView",
    "UserViewSet",
]
