# api/repositories/employee_repository.py

from employees.models import Employee


class EmployeeRepository:

    @staticmethod
    def get_all():
        return Employee.objects.all()

    @staticmethod
    def create(data):
        return Employee.objects.create(**data)

    @staticmethod
    def get_by_id(employee_id):
        return Employee.objects.get(id=employee_id)