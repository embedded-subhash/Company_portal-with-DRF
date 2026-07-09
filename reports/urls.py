from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import DashboardExportView, DashboardView, ReportViewSet

router = DefaultRouter()
router.register("reports", ReportViewSet, basename="report")

urlpatterns = [
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
    path("dashboard/export/", DashboardExportView.as_view(), name="dashboard-export"),
] + router.urls
