from api.repositories.employee_repository import EmployeeRepository


class EmployeeService:
    repository = EmployeeRepository

    @classmethod
    def list_employees(cls):
        return cls.repository.list()

    @classmethod
    def get_employee(cls, pk):
        return cls.repository.get(pk)

    @classmethod
    def create_employee(cls, validated_data):
        return cls.repository.create(validated_data)

    @classmethod
    def update_employee(cls, employee, validated_data):
        return cls.repository.update(employee, validated_data)

    @classmethod
    def delete_employee(cls, employee):
        return cls.repository.delete(employee)
