import random
from datetime import date, timedelta

from django.contrib.auth.models import Group, User
from django.core.management.base import BaseCommand

from employees.models import Attendance, Department, Employee

DEPARTMENTS = [("Engineering", "ENG"), ("Human Resources", "HR"), ("Finance", "FIN"), ("Sales", "SAL")]
DESIGNATIONS = ["Software Engineer", "Senior Engineer", "HR Executive", "Accountant", "Sales Manager"]


class Command(BaseCommand):
    help = "Seeds demo users, groups, departments, employees and attendance records."

    def handle(self, *args, **options):
        for group_name in ["Admin", "HR"]:
            Group.objects.get_or_create(name=group_name)

        if not User.objects.filter(username="admin").exists():
            admin = User.objects.create_superuser("admin", "admin@example.com", "admin12345")
            self.stdout.write("Created superuser 'admin' / 'admin12345'")
        else:
            admin = User.objects.get(username="admin")

        hr_user, created = User.objects.get_or_create(username="hr_user", defaults={"email": "hr@example.com"})
        if created:
            hr_user.set_password("hr12345")
            hr_user.save()
        hr_user.groups.add(Group.objects.get(name="HR"))

        departments = []
        for name, code in DEPARTMENTS:
            dept, _ = Department.objects.get_or_create(name=name, defaults={"code": code})
            departments.append(dept)

        emp_user, created = User.objects.get_or_create(username="emp001", defaults={"email": "emp001@example.com"})
        if created:
            emp_user.set_password("emp12345")
            emp_user.save()

        created_count = 0
        for i in range(1, 21):
            emp_id = f"EMP{i:03d}"
            if Employee.objects.filter(employee_id=emp_id).exists():
                continue
            emp = Employee.objects.create(
                employee_id=emp_id,
                first_name=f"First{i}",
                last_name=f"Last{i}",
                email=f"{emp_id.lower()}@example.com",
                phone=f"90000000{i:02d}",
                department=random.choice(departments),
                designation=random.choice(DESIGNATIONS),
                salary=random.randint(30000, 120000),
                joining_date=date.today() - timedelta(days=random.randint(30, 1500)),
                status="ACTIVE" if i % 6 != 0 else "INACTIVE",
                user=emp_user if i == 1 else None,
            )
            created_count += 1
            for d in range(10):
                Attendance.objects.get_or_create(
                    employee=emp,
                    date=date.today() - timedelta(days=d),
                    defaults={"status": random.choice(["PRESENT", "PRESENT", "PRESENT", "ABSENT", "LEAVE"])},
                )

        self.stdout.write(self.style.SUCCESS(
            f"Seed complete. Departments={len(departments)}, New employees={created_count}, "
            f"Total employees={Employee.objects.count()}"
        ))
