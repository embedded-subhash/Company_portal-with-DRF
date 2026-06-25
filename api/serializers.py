from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from employees.models import Employee
from departments.models import Department
from accounts.models import User


class EmailTokenObtainPairSerializer(TokenObtainPairSerializer):
    username = serializers.CharField(required=False, write_only=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields[self.username_field].required = False

    def validate(self, attrs):
        username = attrs.pop('username', None)

        if username and not attrs.get(self.username_field):
            attrs[self.username_field] = username

        if not attrs.get(self.username_field):
            raise serializers.ValidationError({
                self.username_field: 'This field is required.'
            })

        return super().validate(attrs)


class EmployeeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Employee
        fields = "__all__"


class DepartmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Department
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        exclude = ['password']
