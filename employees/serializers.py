from rest_framework import serializers

from .models import Attendance, Department, Employee


class DepartmentSerializer(serializers.ModelSerializer):
    employee_count = serializers.IntegerField(source="employees.count", read_only=True)

    class Meta:
        model = Department
        fields = ["id", "name", "code", "employee_count"]


class EmployeeSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(read_only=True)
    department_name = serializers.CharField(source="department.name", read_only=True)

    class Meta:
        model = Employee
        fields = [
            "id", "employee_id", "first_name", "last_name", "full_name", "email", "phone",
            "department", "department_name", "designation", "salary", "joining_date", "status",
            "profile_photo", "resume", "aadhaar_document", "pan_document",
            "created_at", "updated_at",
        ]
        read_only_fields = ["created_at", "updated_at"]


class EmployeeSelfServiceSerializer(serializers.ModelSerializer):
    """Restricted serializer for the IsEmployeeReadOnlySelf role - salary/status not writable."""
    full_name = serializers.CharField(read_only=True)

    class Meta:
        model = Employee
        fields = [
            "id", "employee_id", "first_name", "last_name", "full_name", "email", "phone",
            "department", "designation", "salary", "joining_date", "status",
            "profile_photo", "resume", "aadhaar_document", "pan_document",
        ]
        read_only_fields = ["employee_id", "department", "designation", "salary", "joining_date", "status"]


class AttendanceSerializer(serializers.ModelSerializer):
    employee_name = serializers.CharField(source="employee.full_name", read_only=True)

    class Meta:
        model = Attendance
        fields = ["id", "employee", "employee_name", "date", "status"]


class ExcelImportResultSerializer(serializers.Serializer):
    total_rows = serializers.IntegerField()
    created = serializers.IntegerField()
    failed = serializers.IntegerField()
    errors = serializers.ListField(child=serializers.CharField())
