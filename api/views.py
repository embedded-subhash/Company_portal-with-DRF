from django.db.models import Sum, Count
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.permissions import IsAdminOrHRorManager, IsAdmin
from accounts.throttles import ReportRateThrottle
from departments.models import Department
from employees.models import Employee


class DashboardView(APIView):
    """
    GET /api/v1/dashboard/
    Accessible to Admin, HR, and Manager only (Module 12).
    """
    permission_classes = [IsAdminOrHRorManager]
    throttle_classes = [ReportRateThrottle]

    def get(self, request):
        total_employees = Employee.objects.count()
        by_department = (
            Employee.objects.values("department__name")
            .annotate(count=Count("id"))
            .order_by("-count")
        )
        return Response({
            "total_employees": total_employees,
            "total_departments": Department.objects.count(),
            "employees_by_department": list(by_department),
        })


class SalaryReportView(APIView):
    """
    GET /api/v1/reports/salary/
    Admin-only aggregate report.
    """
    permission_classes = [IsAdmin]
    throttle_classes = [ReportRateThrottle]

    def get(self, request):
        summary = Employee.objects.aggregate(
            total_payroll=Sum("salary"), headcount=Count("id")
        )
        by_department = (
            Employee.objects.values("department__name")
            .annotate(total=Sum("salary"), headcount=Count("id"))
            .order_by("-total")
        )
        return Response({
            "summary": summary,
            "by_department": list(by_department),
        })
