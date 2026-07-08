from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView

from accounts.views import APILoginView
from .views import DashboardView, SalaryReportView

urlpatterns = [

    # Authentication APIs
    path(
        "v1/auth/login/",
        APILoginView.as_view(),
        name="api-login"
    ),

    path(
        "v1/auth/refresh/",
        TokenRefreshView.as_view(),
        name="token-refresh"
    ),

    # Employee APIs
    path(
        "v1/employees/",
        include("employees.urls")
    ),

    # Department APIs
    path(
        "v1/departments/",
        include("departments.urls")
    ),

    # Logs APIs
    path(
        "v1/logs/",
        include("logs.urls")
    ),

    # Dashboard
    path(
        "v1/dashboard/",
        DashboardView.as_view(),
        name="dashboard"
    ),

    # Reports
    path(
        "v1/reports/salary/",
        SalaryReportView.as_view(),
        name="salary-report"
    ),
]
