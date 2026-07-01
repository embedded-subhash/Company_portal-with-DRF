from django.db.models import Count, Avg, Sum, Max
from django.db.models.functions import TruncMonth
from django.utils import timezone

from employees.models import Employee
from departments.models import Department


class ReportService:

    @staticmethod
    def top_10_highest_paid_employees():
        return Employee.objects.order_by("-salary")[:10]

    @staticmethod
    def department_wise_employee_count():
        return Department.objects.annotate(
            employee_count=Count("employee")
        )

    @staticmethod
    def monthly_salary_statistics():
        return (
            Employee.objects
            .annotate(
                month=TruncMonth("joining_date")
            )
            .values("month")
            .annotate(
                total_salary=Sum("salary"),
                average_salary=Avg("salary"),
                highest_salary=Max("salary"),
                employee_count=Count("id")
            )
            .order_by("month")
        )

    @staticmethod
    def employees_joined_this_month():
        today = timezone.now()

        return Employee.objects.filter(
            joining_date__year=today.year,
            joining_date__month=today.month
        )