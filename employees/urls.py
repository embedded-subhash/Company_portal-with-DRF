from rest_framework.routers import DefaultRouter

from .views import (
    EmployeeViewSet,
    DepartmentViewSet,
    AttendanceViewSet,
)

router = DefaultRouter()

router.register(
    r"employees",
    EmployeeViewSet,
    basename="employee",
)

router.register(
    r"departments",
    DepartmentViewSet,
    basename="department",
)

router.register(
    r"attendance",
    AttendanceViewSet,
    basename="attendance",
)

urlpatterns = router.urls