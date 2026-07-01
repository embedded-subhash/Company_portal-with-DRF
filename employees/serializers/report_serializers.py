# employees/serializers/report_serializer.py

from rest_framework import serializers


class TopEmployeeSerializer(serializers.Serializer):
    employee_id = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    salary = serializers.DecimalField(
        max_digits=10,
        decimal_places=2
    )


class DepartmentCountSerializer(serializers.Serializer):
    department = serializers.CharField()
    employee_count = serializers.IntegerField()


class MonthlySalarySerializer(serializers.Serializer):
    month = serializers.DateField()
    total_salary = serializers.DecimalField(
        max_digits=15,
        decimal_places=2
    )
    average_salary = serializers.DecimalField(
        max_digits=15,
        decimal_places=2
    )
    highest_salary = serializers.DecimalField(
        max_digits=15,
        decimal_places=2
    )
    employee_count = serializers.IntegerField()