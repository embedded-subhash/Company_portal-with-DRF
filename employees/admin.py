import csv

from django.contrib import admin
from django.http import HttpResponse

from .models import (
    Employee,
    EmployeeProfile,
    BlockedIP
)


@admin.action(description="Mark selected employees as Active")
def activate_employees(modeladmin, request, queryset):

    queryset.update(
        status=True
    )


@admin.action(description="Mark selected employees as Inactive")
def deactivate_employees(modeladmin, request, queryset):

    queryset.update(
        status=False
    )


@admin.action(description="Export selected employees to CSV")
def export_employees_csv(modeladmin, request, queryset):

    response = HttpResponse(
        content_type="text/csv"
    )

    response[
        "Content-Disposition"
    ] = 'attachment; filename="employees.csv"'

    writer = csv.writer(response)

    writer.writerow([
        "Employee ID",
        "First Name",
        "Last Name",
        "Email",
        "Phone",
        "Department",
        "Designation",
        "Salary",
        "Joining Date",
        "Status",
    ])

    for employee in queryset:

        writer.writerow([
            employee.employee_id,
            employee.first_name,
            employee.last_name,
            employee.email,
            employee.phone,
            employee.department.name,
            employee.designation,
            employee.salary,
            employee.joining_date,
            employee.status,
        ])

    return response


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):

    list_display = (
        "employee_id",
        "first_name",
        "last_name",
        "email",
        "department",
        "designation",
        "salary",
        "status",
        "joining_date",
    )

    search_fields = (
        "employee_id",
        "first_name",
        "last_name",
        "email",
    )

    list_filter = (
        "department",
        "status",
        "joining_date",
    )

    date_hierarchy = "joining_date"

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    actions = [
        activate_employees,
        deactivate_employees,
        export_employees_csv,
    ]


@admin.register(EmployeeProfile)
class EmployeeProfileAdmin(admin.ModelAdmin):

    list_display = (
        "employee",
        "blood_group",
        "emergency_contact",
    )

    search_fields = (
        "employee__employee_id",
        "employee__first_name",
        "employee__last_name",
    )


@admin.register(BlockedIP)
class BlockedIPAdmin(admin.ModelAdmin):

    list_display = (
        "ip_address",
        "reason",
        "created_at",
    )

    search_fields = (
        "ip_address",
        "reason",
    )

    readonly_fields = (
        "created_at",
    )
