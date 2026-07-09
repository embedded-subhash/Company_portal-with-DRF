from django.contrib import admin

from .models import Attendance, Department, Employee


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ("name", "code")


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ("employee_id", "full_name", "department", "designation", "status")
    search_fields = ("employee_id", "first_name", "last_name", "email")
    list_filter = ("department", "status")


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ("employee", "date", "status")
    list_filter = ("status", "date")
