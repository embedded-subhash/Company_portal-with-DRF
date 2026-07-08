from datetime import date

from rest_framework import serializers

from departments.models import Department
from employees.models import Employee
from api.validators import (
    validate_employee_id_format,
    validate_joining_date_not_future,
    validate_phone_number,
    validate_salary_non_negative,
)


class DepartmentNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['id', 'name']


class EmployeeSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField(read_only=True)
    experience_years = serializers.SerializerMethodField(read_only=True)
    annual_salary = serializers.SerializerMethodField(read_only=True)
    is_active = serializers.BooleanField(read_only=True)

    department = DepartmentNestedSerializer(read_only=True)
    department_id = serializers.PrimaryKeyRelatedField(
        queryset=Department.objects.all(),
        source='department',
        write_only=True,
        required=False,
        allow_null=True,
    )

    email = serializers.EmailField()
    phone = serializers.CharField(validators=[validate_phone_number])
    employee_id = serializers.CharField(validators=[validate_employee_id_format])
    salary = serializers.DecimalField(max_digits=12, decimal_places=2, validators=[validate_salary_non_negative])
    joining_date = serializers.DateField(validators=[validate_joining_date_not_future])

    class Meta:
        model = Employee
        fields = [
            'id',
            'employee_id',
            'full_name',
            'first_name',
            'last_name',
            'email',
            'phone',
            'department',
            'department_id',
            'designation',
            'manager',
            'experience_years',
            'salary',
            'annual_salary',
            'joining_date',
            'status',
            'is_active',
            'created_at',
        ]
        read_only_fields = ['id', 'created_at']

    def get_full_name(self, obj):
        return getattr(obj, 'full_name', f"{obj.first_name} {obj.last_name}".strip())

    def get_experience_years(self, obj):
        return getattr(obj, 'experience_years', 0)

    def get_annual_salary(self, obj):
        return getattr(obj, 'annual_salary', obj.salary * 12 if obj.salary else 0)

    def validate_email(self, value):
        qs = Employee.objects.filter(email__iexact=value)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError('This email is already in use.')
        return value

    def validate_employee_id(self, value):
        qs = Employee.objects.filter(employee_id__iexact=value)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError('This Employee ID already exists.')
        return value

    def validate(self, attrs):
        return attrs


class EmployeeSummarySerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Employee
        fields = ['id', 'employee_id', 'full_name']

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}".strip()


class EmployeeV2Serializer(EmployeeSerializer):
    department_detail = serializers.SerializerMethodField(read_only=True)
    manager_detail = serializers.SerializerMethodField(read_only=True)

    class Meta(EmployeeSerializer.Meta):
        fields = EmployeeSerializer.Meta.fields + ['department_detail', 'manager_detail']

    def get_department_detail(self, obj):
        if not obj.department_id:
            return None
        return {'id': obj.department.id, 'name': obj.department.name}

    def get_manager_detail(self, obj):
        if not obj.manager_id:
            return None
        return {'id': obj.manager.id, 'name': f"{obj.manager.first_name} {obj.manager.last_name}".strip()}
