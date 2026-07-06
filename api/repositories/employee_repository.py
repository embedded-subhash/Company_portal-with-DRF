from employees.models import Employee


class EmployeeRepository:
    @staticmethod
    def list():
        return Employee.objects.select_related('department', 'manager').all()

    @staticmethod
    def get(pk):
        return Employee.objects.select_related('department', 'manager').get(pk=pk)

    @staticmethod
    def create(validated_data):
        department = validated_data.pop('department', None)
        instance = Employee.objects.create(**validated_data)
        if department is not None:
            instance.department = department
            instance.save(update_fields=['department'])
        return instance

    @staticmethod
    def update(employee, validated_data):
        department = validated_data.pop('department', None)
        for field, value in validated_data.items():
            setattr(employee, field, value)
        if department is not None:
            employee.department = department
        employee.save()
        return employee

    @staticmethod
    def delete(employee):
        employee.delete()