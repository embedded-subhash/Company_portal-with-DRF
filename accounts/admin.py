from django.contrib import admin
from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'email',
        'employee_id',
        'role',
        'is_active',
        'is_staff'
    )

    search_fields = (
        'email',
        'employee_id'
    )

    list_filter = (
        'role',
        'is_active'
    )