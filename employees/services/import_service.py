import pandas as pd

from employees.models import Employee
from employees.tasks import send_welcome_email
from departments.models import Department


class EmployeeImportService:

    @staticmethod
    def import_employees(file):

        df = pd.read_excel(file)

        imported_count = 0

        for _, row in df.iterrows():

            department, _ = Department.objects.get_or_create(
                name=row["department"]
            )

            employee = Employee.objects.create(
                employee_id=row["employee_id"],
                first_name=row["first_name"],
                last_name=row["last_name"],
                email=row["email"],
                phone=row["phone"],
                salary=row["salary"],
                joining_date=row["joining_date"],
                designation=row["designation"],
                department=department,
            )

            # Queue welcome email in background
            send_welcome_email.delay(employee.id)

            imported_count += 1

        return {
            "status": "SUCCESS",
            "imported_count": imported_count
        }