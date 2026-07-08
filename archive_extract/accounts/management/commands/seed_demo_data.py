from datetime import date

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from accounts.models import UserProfile
from departments.models import Department
from employees.models import Employee, Skill


class Command(BaseCommand):
    help = "Seeds demo users, departments, skills, and employees for the HRMS API."

    def handle(self, *args, **options):
        # --- Departments ---------------------------------------------------
        engineering, _ = Department.objects.get_or_create(
            name="Engineering", defaults={"code": "ENG", "description": "Product engineering team."}
        )
        hr_dept, _ = Department.objects.get_or_create(
            name="Human Resources", defaults={"code": "HR", "description": "People operations."}
        )

        # --- Skills ----------------------------------------------------------
        python_skill, _ = Skill.objects.get_or_create(name="Python")
        django_skill, _ = Skill.objects.get_or_create(name="Django")

        # --- Users: admin / hr / employee -----------------------------------
        admin_user, created = User.objects.get_or_create(
            username="admin", defaults={"email": "admin@example.com", "is_superuser": True, "is_staff": True}
        )
        if created:
            admin_user.set_password("Admin@12345")
            admin_user.save()
        UserProfile.objects.update_or_create(user=admin_user, defaults={"role": "admin"})

        hr_user, created = User.objects.get_or_create(
            username="hr_user", defaults={"email": "hr@example.com"}
        )
        if created:
            hr_user.set_password("Hr@123456")
            hr_user.save()
        UserProfile.objects.update_or_create(user=hr_user, defaults={"role": "hr"})

        emp_user, created = User.objects.get_or_create(
            username="ajay.kumar", defaults={"email": "ajay.kumar@example.com", "first_name": "Ajay", "last_name": "Kumar"}
        )
        if created:
            emp_user.set_password("Employee@123")
            emp_user.save()
        UserProfile.objects.update_or_create(user=emp_user, defaults={"role": "employee"})

        # --- Sample employee record -------------------------------------------
        employee, _ = Employee.objects.update_or_create(
            employee_id="EMP00001",
            defaults=dict(
                user=emp_user,
                first_name="Ajay",
                last_name="Kumar",
                email="ajay.kumar@example.com",
                phone="9876543210",
                department=engineering,
                designation="Software Engineer",
                salary=80000,
                joining_date=date(2022, 6, 15),
                status=Employee.Status.ACTIVE,
            ),
        )
        employee.skills.set([python_skill, django_skill])

        self.stdout.write(self.style.SUCCESS("Demo data seeded successfully."))
        self.stdout.write("  admin      / Admin@12345")
        self.stdout.write("  hr_user    / Hr@123456")
        self.stdout.write("  ajay.kumar / Employee@123")
