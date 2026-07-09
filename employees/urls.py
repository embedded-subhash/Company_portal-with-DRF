from rest_framework.routers import DefaultRouter

from .views import AttendanceViewSet, DepartmentViewSet, EmployeeViewSet

router = DefaultRouter()
router.register("employees", EmployeeViewSet, basename="employee")
router.register("departments", DepartmentViewSet, basename="department")
router.register("attendance", AttendanceViewSet, basename="attendance")

urlpatterns = router.urls
