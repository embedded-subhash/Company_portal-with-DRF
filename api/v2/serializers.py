"""
API v2 serializers.

V2 extends V1's basic employee data with: Department, Manager, Skills,
and Profile details (nested/related data), demonstrating API versioning
(Module 10).
"""

from rest_framework import serializers

from employees.models import Employee, Skill
from api.v1.serializers import DepartmentNestedSerializer


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ["id", "name"]


class ManagerNestedSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = Employee
        fields = ["id", "employee_id", "full_name", "designation"]

    def get_full_name(self, obj):
        return obj.full_name


class EmployeeProfileSerializer(serializers.Serializer):
    """Flattened 'profile' block requested for v2 (contact + tenure info)."""

    email = serializers.EmailField()
    phone = serializers.CharField()
    joining_date = serializers.DateField()
    experience_years = serializers.IntegerField()
    status = serializers.CharField()


class EmployeeSerializerV2(serializers.ModelSerializer):
    """
    v2 Employee representation:

        {
            "id": 1,
            "employee_id": "EMP00001",
            "full_name": "Ajay Kumar",
            "department": {"id": 1, "name": "Engineering"},
            "manager": {"id": 3, "employee_id": "EMP00003", "full_name": "...", "designation": "..."},
            "skills": [{"id": 1, "name": "Python"}, ...],
            "profile": {"email": "...", "phone": "...", "joining_date": "...", ...},
            "annual_salary": 960000,
            "is_active": true
        }
    """

    full_name = serializers.SerializerMethodField()
    annual_salary = serializers.SerializerMethodField()
    is_active = serializers.BooleanField(read_only=True)

    department = DepartmentNestedSerializer(read_only=True)
    manager = ManagerNestedSerializer(read_only=True)
    skills = SkillSerializer(many=True, read_only=True)
    skill_ids = serializers.PrimaryKeyRelatedField(
        queryset=Skill.objects.all(), source="skills", many=True, write_only=True, required=False
    )
    profile = serializers.SerializerMethodField()

    class Meta:
        model = Employee
        fields = [
            "id", "employee_id", "full_name", "department", "designation",
            "manager", "skills", "skill_ids", "profile", "annual_salary", "is_active",
        ]

    def get_full_name(self, obj):
        return obj.full_name

    def get_annual_salary(self, obj):
        return obj.annual_salary

    def get_profile(self, obj):
        return EmployeeProfileSerializer(
            {
                "email": obj.email,
                "phone": obj.phone,
                "joining_date": obj.joining_date,
                "experience_years": obj.experience_years,
                "status": obj.status,
            }
        ).data
