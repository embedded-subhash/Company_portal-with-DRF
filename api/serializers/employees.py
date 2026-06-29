from rest_framework import serializers

from employees.models import Employee


class EmployeeSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Employee
        fields = [
            "id",
            "employee_id",
            "first_name",
            "last_name",
            "name",
            "email",
            "phone",
            "salary",
            "joining_date",
            "designation",
            "department",
            "manager",
            "profile_image",
            "status",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

    def get_name(self, obj):
        return f"{obj.first_name} {obj.last_name}".strip()


class EmployeeSummarySerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    class Meta:
        model = Employee
        fields = ["id", "name"]

    def get_name(self, obj):
        return f"{obj.first_name} {obj.last_name}".strip()


class EmployeeV2Serializer(EmployeeSerializer):
    department_detail = serializers.SerializerMethodField(read_only=True)
    manager = serializers.SerializerMethodField(read_only=True)

    class Meta(EmployeeSerializer.Meta):
        fields = EmployeeSerializer.Meta.fields + [
            "department_detail",
            "manager",
        ]

    def get_department_detail(self, obj):
        if not obj.department_id:
            return None

        return {
            "id": obj.department.id,
            "name": obj.department.name,
        }

    def get_manager(self, obj):
        if not obj.manager_id:
            return None

        return {
            "id": obj.manager.id,
            "name": f"{obj.manager.first_name} {obj.manager.last_name}".strip(),
        }
