from rest_framework import serializers

from departments.models import Department
from .employees import EmployeeSummarySerializer


class DepartmentSerializer(serializers.ModelSerializer):
    employees = EmployeeSummarySerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = Department
        fields = [
            "id",
            "name",
            "description",
            "employees",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]
