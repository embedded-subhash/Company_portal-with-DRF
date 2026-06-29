from django.contrib import admin

from .models import AuditLog


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "action",
        "module",
        "ip_address",
        "timestamp",
    )
    list_filter = ("action", "module", "timestamp")
    search_fields = ("user__email", "action", "module", "ip_address")
    readonly_fields = (
        "user",
        "action",
        "module",
        "ip_address",
        "timestamp",
    )
