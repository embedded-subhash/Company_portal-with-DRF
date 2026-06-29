from django.db import transaction

from employees.models import Employee
from payroll.models import Payroll


class PayrollService:

    @staticmethod
    @transaction.atomic
    def process_salary(employee_id, month, increment):

        employee = Employee.objects.get(
            employee_id=employee_id
        )

        employee.salary += increment
        employee.save()

        Payroll.objects.create(
            employee=employee,
            month=month,
            net_salary=employee.salary
        )

        return employee