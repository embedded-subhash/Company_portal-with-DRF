from datetime import date

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

from departments.models import Department
from employees.models import Employee

User = get_user_model()


class Command(BaseCommand):
    help = "Seed demo users (one per role) and employee records for manual/API testing."

    def handle(self, *args, **options):
        dept, _ = Department.objects.get_or_create(name="Engineering", code="ENG")
        dept2, _ = Department.objects.get_or_create(name="Human Resources", code="HR")

        users = [
            ("admin_user", "admin@company-portal.local", User.Role.ADMIN, "EMP00001", dept),
            ("hr_user", "hr@company-portal.local", User.Role.HR, "EMP00002", dept2),
            ("manager_user", "manager@company-portal.local", User.Role.MANAGER, "EMP00003", dept),
            ("employee_user", "employee@company-portal.local", User.Role.EMPLOYEE, "EMP00004", dept),
            ("employee_user_2", "employee2@company-portal.local", User.Role.EMPLOYEE, "EMP00005", dept),
        ]

        for username, email, role, emp_id, department in users:
            user, created = User.objects.get_or_create(
                username=username, defaults={"email": email, "role": role}
            )
            if created:
                user.set_password("Str0ngP@ssw0rd!")
                user.is_staff = role == User.Role.ADMIN
                user.is_superuser = role == User.Role.ADMIN
                user.save()
                self.stdout.write(self.style.SUCCESS(f"Created user {username} ({role})"))
            else:
                self.stdout.write(f"User {username} already exists, skipping")

            Employee.objects.get_or_create(
                user=user,
                defaults={
                    "employee_id": emp_id,
                    "department": department,
                    "designation": role.title(),
                    "salary": 55000,
                    "joining_date": date(2024, 1, 15),
                },
            )

        self.stdout.write(self.style.SUCCESS("Seed data ready. Password for all users: Str0ngP@ssw0rd!"))
