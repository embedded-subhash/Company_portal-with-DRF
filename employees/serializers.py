from django.contrib.auth import get_user_model
from rest_framework import serializers

from accounts.validators import (
    validate_employee_id, validate_phone_number, validate_salary,
    validate_joining_date, validate_profile_image,
)
from .models import Employee

User = get_user_model()


class EmployeeSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)
    email = serializers.EmailField(source="user.email", read_only=True)
    phone = serializers.CharField(source="user.phone", validators=[validate_phone_number], required=False)
    employee_id = serializers.CharField(validators=[validate_employee_id])
    salary = serializers.DecimalField(max_digits=12, decimal_places=2, validators=[validate_salary])
    joining_date = serializers.DateField(validators=[validate_joining_date])

    class Meta:
        model = Employee
        fields = [
            "id", "user", "username", "email", "phone", "employee_id", "department",
            "designation", "salary", "joining_date", "profile_image", "created_at", "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]
        extra_kwargs = {"user": {"write_only": True}}

    def update(self, instance, validated_data):
        user_data = validated_data.pop("user", None)
        if user_data and "phone" in user_data:
            instance.user.phone = user_data["phone"]
            instance.user.save(update_fields=["phone"])
        return super().update(instance, validated_data)


class ProfileImageUploadSerializer(serializers.Serializer):
    profile_image = serializers.ImageField(validators=[validate_profile_image])

    def save(self, **kwargs):
        employee = self.context["employee"]
        employee.profile_image = self.validated_data["profile_image"]
        employee.save(update_fields=["profile_image", "updated_at"])
        return employee
