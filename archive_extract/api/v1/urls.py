from django.urls import include, path
from rest_framework.routers import DefaultRouter

from reports.views import AuditLogViewSet

from .views import (
    DashboardStatsView,
    DepartmentViewSet,
    EmployeeProfileView,
    EmployeeViewSet,
)

router = DefaultRouter()
router.register(r"employees", EmployeeViewSet, basename="employee")
router.register(r"departments", DepartmentViewSet, basename="department")
router.register(r"audit-logs", AuditLogViewSet, basename="audit-log")

urlpatterns = [
    path("auth/", include("accounts.urls")),
    path("employees/profile/me/", EmployeeProfileView.as_view(), name="employee-profile-me"),
    path("dashboard/stats/", DashboardStatsView.as_view(), name="dashboard-stats"),
    path("", include(router.urls)),
]
