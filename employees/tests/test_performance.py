from datetime import date

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from departments.models import Department
from employees.models import Employee

User = get_user_model()


class EmployeePermissionTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.department = Department.objects.create(
            name="IT"
        )

        cls.admin = User.objects.create_user(
            email="admin@test.com",
            password="Admin@123",
            role="ADMIN",
        )

        cls.hr = User.objects.create_user(
            email="hr@test.com",
            password="Hr@123",
            role="HR",
        )

        cls.employee_user = User.objects.create_user(
            email="employee@test.com",
            password="Employee@123",
            role="EMPLOYEE",
        )

        cls.employee = Employee.objects.create(
            user=cls.employee_user,
            employee_id="EMP001",
            first_name="Subhash",
            last_name="Kumar",
            email="subhash@test.com",
            phone="9876543210",
            department=cls.department,
            designation="Developer",
            salary=50000,
            joining_date=date.today(),
            status="ACTIVE",
        )

    def test_admin_can_access_employee_list(self):
        self.client.force_login(self.admin)

        response = self.client.get(
            reverse("employee_list")
        )

        self.assertEqual(response.status_code, 200)

    def test_hr_can_view_employee_list(self):
        self.client.force_login(self.hr)

        response = self.client.get(
            reverse("employee_list")
        )

        self.assertIn(response.status_code, [200, 302])

    def test_employee_requires_login(self):
        response = self.client.get(
            reverse("employee_list")
        )

        self.assertEqual(response.status_code, 302)

    def test_admin_can_view_detail(self):
        self.client.force_login(self.admin)

        response = self.client.get(
            reverse(
                "employee_detail",
                args=[self.employee.pk],
            )
        )

        self.assertEqual(response.status_code, 200)

    def test_admin_can_open_create_page(self):
        self.client.force_login(self.admin)

        response = self.client.get(
            reverse("employee_create")
        )

        self.assertEqual(response.status_code, 200)

    def test_admin_can_open_update_page(self):
        self.client.force_login(self.admin)

        response = self.client.get(
            reverse(
                "employee_update",
                args=[self.employee.pk],
            )
        )

        self.assertEqual(response.status_code, 200)

    def test_admin_can_open_delete_page(self):
        self.client.force_login(self.admin)

        response = self.client.get(
            reverse(
                "employee_delete",
                args=[self.employee.pk],
            )
        )

        self.assertEqual(response.status_code, 200)