# employees/services/transaction_service.py

from django.db import transaction

from employees.models import Employee
from departments.models import Department


class TransactionService:

    @staticmethod
    @transaction.atomic
    def create_employee(data):

        department = Department.objects.get(
            id=data["department_id"]
        )

        employee = Employee.objects.create(
            employee_id=data["employee_id"],
            first_name=data["first_name"],
            last_name=data["last_name"],
            email=data["email"],
            phone=data["phone"],
            salary=data["salary"],
            joining_date=data["joining_date"],
            designation=data["designation"],
            department=department
        )

        return employee

    @staticmethod
    @transaction.atomic
    def test_rollback(data):

        department = Department.objects.get(
            id=data["department_id"]
        )

        employee = Employee.objects.create(
            employee_id=data["employee_id"],
            first_name=data["first_name"],
            last_name=data["last_name"],
            email=data["email"],
            phone=data["phone"],
            salary=data["salary"],
            joining_date=data["joining_date"],
            designation=data["designation"],
            department=department
        )

        # Force an error
        raise Exception("Testing transaction rollback")

        return employee