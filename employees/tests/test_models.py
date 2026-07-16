from decimal import Decimal
from datetime import date, timedelta

from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import TestCase

from departments.models import Department
from employees.models import Employee


class EmployeeModelTests(TestCase):
    def setUp(self):
        self.department = Department.objects.create(name="Engineering", description="Engineering team")

    def test_employee_creation_saves_expected_fields(self):
        employee = Employee.objects.create(
            employee_id="EMP00001",
            first_name="Asha",
            last_name="Mohan",
            email="asha@example.com",
            phone="9876543210",
            department=self.department,
            designation="Developer",
            salary=Decimal("120000.00"),
            joining_date=date(2024, 1, 1),
        )
        self.assertEqual(employee.full_name, "Asha Mohan")
        self.assertEqual(employee.department.name, "Engineering")

    def test_duplicate_employee_id_is_rejected(self):
        Employee.objects.create(
            employee_id="EMP00002",
            first_name="Asha",
            last_name="Mohan",
            email="asha2@example.com",
            phone="9876543210",
            department=self.department,
            designation="Developer",
            salary=Decimal("120000.00"),
            joining_date=date(2024, 1, 1),
        )
        with self.assertRaises(IntegrityError):
            Employee.objects.create(
                employee_id="EMP00002",
                first_name="Bharat",
                last_name="Rao",
                email="bharat@example.com",
                phone="9876543211",
                department=self.department,
                designation="Manager",
                salary=Decimal("140000.00"),
                joining_date=date(2024, 2, 1),
            )

    def test_duplicate_email_is_rejected(self):
        Employee.objects.create(
            employee_id="EMP00003",
            first_name="Asha",
            last_name="Mohan",
            email="asha3@example.com",
            phone="9876543210",
            department=self.department,
            designation="Developer",
            salary=Decimal("120000.00"),
            joining_date=date(2024, 1, 1),
        )
        with self.assertRaises(IntegrityError):
            Employee.objects.create(
                employee_id="EMP00004",
                first_name="Bharat",
                last_name="Rao",
                email="asha3@example.com",
                phone="9876543211",
                department=self.department,
                designation="Manager",
                salary=Decimal("140000.00"),
                joining_date=date(2024, 2, 1),
            )

    def test_salary_must_be_positive(self):
        employee = Employee(
            employee_id="EMP00005",
            first_name="Asha",
            last_name="Mohan",
            email="asha5@example.com",
            phone="9876543210",
            department=self.department,
            designation="Developer",
            salary=Decimal("0"),
            joining_date=date(2024, 1, 1),
        )
        with self.assertRaises(ValidationError):
            employee.save()

    def test_joining_date_cannot_be_future(self):
        employee = Employee(
            employee_id="EMP00006",
            first_name="Asha",
            last_name="Mohan",
            email="asha6@example.com",
            phone="9876543210",
            department=self.department,
            designation="Developer",
            salary=Decimal("120000.00"),
            joining_date=date.today() + timedelta(days=1),
        )
        with self.assertRaises(ValidationError):
            employee.save()


class EmployeeOrmTests(TestCase):
    def setUp(self):
        self.department = Department.objects.create(name="HR", description="HR team")

    def test_crud_and_query_operations(self):
        employee = Employee.objects.create(
            employee_id="EMP00007",
            first_name="Kavi",
            last_name="Sharma",
            email="kavi@example.com",
            phone="9898989898",
            department=self.department,
            designation="HR Specialist",
            salary=Decimal("120000.00"),
            joining_date=date(2023, 1, 1),
        )
        self.assertEqual(Employee.objects.count(), 1)

        employee.designation = "Senior HR Specialist"
        employee.save(update_fields=["designation"])
        self.assertEqual(Employee.objects.get(pk=employee.pk).designation, "Senior HR Specialist")

        employee.delete()
        self.assertFalse(Employee.objects.filter(pk=employee.pk).exists())

    def test_search_and_filter_by_department_and_status(self):
        Employee.objects.create(
            employee_id="EMP00008",
            first_name="Nina",
            last_name="Dutta",
            email="nina@example.com",
            phone="9876543212",
            department=self.department,
            designation="Analyst",
            salary=Decimal("90000.00"),
            joining_date=date(2023, 6, 1),
            status="ACTIVE",
        )
        Employee.objects.create(
            employee_id="EMP00009",
            first_name="Oscar",
            last_name="Lee",
            email="oscar@example.com",
            phone="9876543213",
            department=self.department,
            designation="Analyst",
            salary=Decimal("95000.00"),
            joining_date=date(2023, 7, 1),
            status="INACTIVE",
        )
        results = Employee.objects.filter(first_name__icontains="ni")
        self.assertEqual(results.count(), 1)
        filtered = Employee.objects.filter(department=self.department, status="ACTIVE")
        self.assertTrue(filtered.exists())
        self.assertEqual(filtered.first().first_name, "Nina")
