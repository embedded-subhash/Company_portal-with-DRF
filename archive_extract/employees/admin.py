from django.contrib import admin
from .models import Employee, Skill


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    search_fields = ("name",)


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = (
        "employee_id", "first_name", "last_name", "department",
        "designation", "salary", "status", "joining_date",
    )
    list_filter = ("status", "department", "designation")
    search_fields = ("employee_id", "first_name", "last_name", "email", "phone")
