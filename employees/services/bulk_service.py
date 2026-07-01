from datetime import date

from employees.models import Employee
from departments.models import Department


class BulkService:

    @staticmethod
    def create_test_employees():

        department = Department.objects.get(id=1)

        employees = []

        for i in range(1, 6):

            employees.append(
                Employee(
                    employee_id=f"EMP_BULK_{i}",
                    first_name=f"User{i}",
                    last_name="Test",
                    email=f"user{i}@gmail.com",
                    phone="9999999999",
                    salary=50000 + i * 1000,
                    joining_date=date.today(),
                    designation="Developer",
                    department=department
                )
            )

        Employee.objects.bulk_create(employees)

        return "Employees created"

    @staticmethod
    def increase_salary():

        employees = Employee.objects.filter(
            employee_id__startswith="EMP_BULK"
        )

        for employee in employees:
            employee.salary += 5000

        Employee.objects.bulk_update(
            employees,
            ["salary"]
        )

        return "Salaries updated"