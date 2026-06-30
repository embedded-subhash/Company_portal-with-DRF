import pandas as pd

from employees.models import Employee
from employees.tasks import send_welcome_email


class EmployeeImportService:

    @staticmethod
    def import_employees(file):

        df = pd.read_excel(file)

        imported_count = 0

        for _, row in df.iterrows():

            employee = Employee.objects.create(
                employee_id=row["employee_id"],
                first_name=row["first_name"],
                last_name=row["last_name"],
                email=row["email"],
            )

            send_welcome_email.delay(employee.id)

            imported_count += 1

        return {
            "imported_count": imported_count
        }