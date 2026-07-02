from faker import Faker

from django.core.management.base import BaseCommand

from departments.models import Department
from employees.models import Employee


fake = Faker()


class Command(BaseCommand):

    help = "Generate departments and employees"

    def handle(self, *args, **kwargs):

        departments = []

        for i in range(10):

            department, created = Department.objects.get_or_create(
                name=f"Department {i + 1}"
            )

            departments.append(department)

        for i in range(100):

            Employee.objects.create(
                employee_id=f"EMP{i + 1000}",
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                email=fake.unique.email(),
                phone=fake.phone_number()[:15],
                salary=fake.random_int(
                    min=30000,
                    max=150000
                ),
                joining_date=fake.date_this_decade(),
                designation="Software Engineer",
                department=fake.random_element(departments)
            )

        self.stdout.write(
            self.style.SUCCESS(
                "Seed data created successfully."
            )
        )