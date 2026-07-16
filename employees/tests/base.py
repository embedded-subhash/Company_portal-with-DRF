from django.test import TestCase
from departments.models import Department
from employees.models import Employee

class BaseTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):

        cls.department = Department.objects.create(
            name="IT"
        )

        cls.employee = Employee.objects.create(
            employee_id="EMP001",
            first_name="Subhash",
            last_name="Kumar",
            email="subhash@test.com",
            phone="9876543210",
            designation="Software Engineer",
            salary=50000,
            department=cls.department
        )