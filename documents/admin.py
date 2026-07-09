from django.contrib import admin

from .models import EmployeeDocument


@admin.register(EmployeeDocument)
class EmployeeDocumentAdmin(admin.ModelAdmin):
    list_display = ("employee", "document_name", "document_type", "uploaded_by", "uploaded_at")
    list_filter = ("document_type",)
    search_fields = ("document_name", "employee__employee_id")
