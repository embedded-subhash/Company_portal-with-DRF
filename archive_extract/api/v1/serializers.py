"""
API v1 serializers.

v1 exposes the basic employee data shape:

    {
        "employee_id": "EMP001",
        "full_name": "Ajay Kumar",
        "department": {"id": 1, "name": "Engineering"},
        "experience_years": 4,
        "annual_salary": 960000,
        "is_active": true
    }
"""

from django.contrib.auth.models import User
from rest_framework import serializers

from departments.models import Department
from employees.models import Employee
from api.validators import (
    validate_employee_id_format,
    validate_joining_date_not_future,
    validate_phone_number,
    validate_salary_non_negative,
)


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ["id", "name", "code", "description", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]


class DepartmentNestedSerializer(serializers.ModelSerializer):
    """Minimal nested representation used inside EmployeeSerializer."""

    class Meta:
        model = Department
        fields = ["id", "name"]


class EmployeeSerializer(serializers.ModelSerializer):
    """
    Read/write serializer for the Employee resource (API v1).

    - full_name, experience_years, annual_salary, is_active are computed
      (SerializerMethodField / model properties) -> read-only.
    - department is a nested read representation, but writes accept
      department_id.
    """

    full_name = serializers.SerializerMethodField()
    experience_years = serializers.SerializerMethodField()
    annual_salary = serializers.SerializerMethodField()
    is_active = serializers.BooleanField(read_only=True)

    department = DepartmentNestedSerializer(read_only=True)
    department_id = serializers.PrimaryKeyRelatedField(
        queryset=Department.objects.all(), source="department", write_only=True, required=False, allow_null=True
    )

    # write-only password-like fields are not needed here, but phone/email
    # get explicit field-level validation per Module 11.
    email = serializers.EmailField()
    phone = serializers.CharField(validators=[validate_phone_number])
    employee_id = serializers.CharField(validators=[validate_employee_id_format])
    salary = serializers.DecimalField(
        max_digits=12, decimal_places=2, validators=[validate_salary_non_negative]
    )
    joining_date = serializers.DateField(validators=[validate_joining_date_not_future])

    class Meta:
        model = Employee
        fields = [
            "id",
            "employee_id",
            "full_name",
            "first_name",
            "last_name",
            "email",
            "phone",
            "department",
            "department_id",
            "designation",
            "manager",
            "experience_years",
            "salary",
            "annual_salary",
            "joining_date",
            "status",
            "is_active",
            "created_at",
        ]
        read_only_fields = ["id", "created_at"]

    # --- SerializerMethodField implementations -----------------------------
    def get_full_name(self, obj):
        return obj.full_name

    def get_experience_years(self, obj):
        return obj.experience_years

    def get_annual_salary(self, obj):
        return obj.annual_salary

    # --- Field-level validation ---------------------------------------------
    def validate_email(self, value):
        qs = Employee.objects.filter(email__iexact=value)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError("This email is already in use.")
        return value

    def validate_employee_id(self, value):
        qs = Employee.objects.filter(employee_id__iexact=value)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError("This Employee ID already exists.")
        return value

    # --- Object-level validation ---------------------------------------------
    def validate(self, attrs):
        manager = attrs.get("manager")
        if manager and self.instance and manager.pk == self.instance.pk:
            raise serializers.ValidationError({"manager": "An employee cannot be their own manager."})
        return attrs


class EmployeeListSerializer(EmployeeSerializer):
    """A lighter serializer for list views (optional optimization)."""

    class Meta(EmployeeSerializer.Meta):
        fields = [
            "id", "employee_id", "full_name", "department", "designation",
            "experience_years", "annual_salary", "status", "is_active",
        ]


class BulkEmployeeCreateSerializer(serializers.ListSerializer):
    child = EmployeeSerializer()


class EmployeeBulkUpdateItemSerializer(serializers.Serializer):
    """One row inside a bulk-update payload: {"id": 5, ...fields to update}."""

    id = serializers.IntegerField()

    def validate_id(self, value):
        if not Employee.objects.filter(pk=value).exists():
            raise serializers.ValidationError(f"Employee with id {value} does not exist.")
        return value


class DashboardStatsSerializer(serializers.Serializer):
    total_employees = serializers.IntegerField()
    active_employees = serializers.IntegerField()
    inactive_employees = serializers.IntegerField()
    department_count = serializers.IntegerField()
    new_joiners_last_30_days = serializers.IntegerField()
    average_salary = serializers.DecimalField(max_digits=12, decimal_places=2)
