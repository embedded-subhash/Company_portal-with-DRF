from django.contrib import admin
from .models import SecurityLog


@admin.register(SecurityLog)
class SecurityLogAdmin(admin.ModelAdmin):
    list_display = ("timestamp", "action", "status", "actor_identifier", "ip_address", "path")
    list_filter = ("action", "status")
    search_fields = ("actor_identifier", "ip_address", "detail")
    readonly_fields = [f.name for f in SecurityLog._meta.fields]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False
