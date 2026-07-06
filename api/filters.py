"""
Filtering, used with django-filter's DjangoFilterBackend.

Examples:
    GET /api/v1/employees/?department=IT
    GET /api/v1/employees/?status=active
    GET /api/v1/employees/?salary__gte=50000
    GET /api/v1/employees/?salary__lte=100000
    GET /api/v1/employees/?joining_date_after=2024-01-01
    GET /api/v1/employees/?joining_date_before=2024-12-31
    GET /api/v1/employees/?designation=Manager
"""

import django_filters

from employees.models import Employee


class EmployeeFilter(django_filters.FilterSet):
    # Filter by department name (case-insensitive) or by id.
    department = django_filters.CharFilter(field_name="department__name", lookup_expr="iexact")
    department_id = django_filters.NumberFilter(field_name="department__id")

    status = django_filters.ChoiceFilter(choices=Employee.Status.choices)

    # Salary range: ?salary__gte=50000&salary__lte=100000
    salary__gte = django_filters.NumberFilter(field_name="salary", lookup_expr="gte")
    salary__lte = django_filters.NumberFilter(field_name="salary", lookup_expr="lte")

    # Joining date range: ?joining_date_after=...&joining_date_before=...
    joining_date_after = django_filters.DateFilter(field_name="joining_date", lookup_expr="gte")
    joining_date_before = django_filters.DateFilter(field_name="joining_date", lookup_expr="lte")

    designation = django_filters.CharFilter(field_name="designation", lookup_expr="icontains")

    class Meta:
        model = Employee
        fields = [
            "department", "department_id", "status",
            "salary__gte", "salary__lte",
            "joining_date_after", "joining_date_before",
            "designation",
        ]
