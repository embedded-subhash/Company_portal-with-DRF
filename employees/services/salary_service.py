from django.db import transaction

from employees.models import Employee


class SalaryService:

    @staticmethod
    @transaction.atomic
    def increase_salary(employee_id, amount):

        employee = Employee.objects.select_for_update().get(
            employee_id=employee_id
        )

        employee.salary += amount

        employee.save()

        return employee