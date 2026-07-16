from datetime import date, timedelta

from django.test import TestCase

from departments.models import Department
from employees.forms import EmployeeForm
from employees.models import Employee


class EmployeeFormTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.department = Department.objects.create(
            name="IT"
        )

        Employee.objects.create(
            employee_id="EMP001",
            first_name="John",
            last_name="Doe",
            email="john@gmail.com",
            phone="9876543210",
            department=cls.department,
            designation="Developer",
            salary=50000,
            joining_date=date.today(),
            status="ACTIVE",
        )

    def get_valid_data(self):
        return {
            "employee_id": "EMP002",
            "first_name": "Subhash",
            "last_name": "Kumar",
            "email": "subhash@gmail.com",
            "phone": "9999999999",
            "department": self.department.id,
            "designation": "Python Developer",
            "salary": 60000,
            "joining_date": date.today(),
            "status": "ACTIVE",
        }

    def test_valid_form(self):
        form = EmployeeForm(data=self.get_valid_data())
        self.assertTrue(form.is_valid())

    def test_invalid_employee_id(self):
        data = self.get_valid_data()
        data["employee_id"] = "100"

        form = EmployeeForm(data=data)

        self.assertFalse(form.is_valid())
        self.assertIn("employee_id", form.errors)

    def test_duplicate_email(self):
        data = self.get_valid_data()
        data["email"] = "john@gmail.com"

        form = EmployeeForm(data=data)

        self.assertFalse(form.is_valid())
        self.assertIn("email", form.errors)

    def test_invalid_phone(self):
        data = self.get_valid_data()
        data["phone"] = "12345"

        form = EmployeeForm(data=data)

        self.assertFalse(form.is_valid())
        self.assertIn("phone", form.errors)

    def test_salary_less_than_minimum(self):
        data = self.get_valid_data()
        data["salary"] = 5000

        form = EmployeeForm(data=data)

        self.assertFalse(form.is_valid())
        self.assertIn("salary", form.errors)

    def test_salary_greater_than_maximum(self):
        data = self.get_valid_data()
        data["salary"] = 600000

        form = EmployeeForm(data=data)

        self.assertFalse(form.is_valid())
        self.assertIn("salary", form.errors)

    def test_future_joining_date(self):
        data = self.get_valid_data()
        data["joining_date"] = date.today() + timedelta(days=10)

        form = EmployeeForm(data=data)

        self.assertFalse(form.is_valid())
        self.assertIn("joining_date", form.errors)