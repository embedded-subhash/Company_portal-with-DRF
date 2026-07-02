from pathlib import Path

from django.core.management.base import BaseCommand
from django.db.models import Avg, Max, Min

from employees.models import Employee
from departments.models import Department


class Command(BaseCommand):

    help = "Generate HRMS reports"

    def handle(self, *args, **kwargs):

        report_dir = Path("reports")
        report_dir.mkdir(exist_ok=True)

        employee_count = Employee.objects.count()

        department_count = Department.objects.count()

        salary_stats = Employee.objects.aggregate(
            average_salary=Avg("salary"),
            max_salary=Max("salary"),
            min_salary=Min("salary")
        )

        report_file = report_dir / "employee_report.txt"

        with open(report_file, "w") as file:

            file.write("=== HRMS REPORT ===\n\n")

            file.write(
                f"Total Employees: {employee_count}\n"
            )

            file.write(
                f"Total Departments: {department_count}\n"
            )

            file.write(
                f"Average Salary: "
                f"{salary_stats['average_salary']}\n"
            )

            file.write(
                f"Maximum Salary: "
                f"{salary_stats['max_salary']}\n"
            )

            file.write(
                f"Minimum Salary: "
                f"{salary_stats['min_salary']}\n"
            )

        self.stdout.write(
            self.style.SUCCESS(
                "Employee report generated successfully."
            )
        )