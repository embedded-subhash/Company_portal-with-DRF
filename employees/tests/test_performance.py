from datetime import date

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework import status
from rest_framework.test import APITestCase

from departments.models import Department
from employees.models import Employee

User = get_user_model()


class EmployeePermissionTests(APITestCase):

    @classmethod
    def setUpTestData(cls):

        # Department
        cls.department = Department.objects.create(
            name="IT"
        )

        # Create Groups
        cls.admin_group, _ = Group.objects.get_or_create(
            name="Admin"
        )

        cls.hr_group, _ = Group.objects.get_or_create(
            name="HR"
        )

        # Admin User
        cls.admin = User.objects.create_user(
            email="admin@test.com",
            password="Admin@123",
            role="ADMIN",
        )

        cls.admin.groups.add(cls.admin_group)

        # HR User
        cls.hr = User.objects.create_user(
            email="hr@test.com",
            password="Hr@123",
            role="HR",
        )

        cls.hr.groups.add(cls.hr_group)

        # Employee User
        cls.employee_user = User.objects.create_user(
            email="employee@test.com",
            password="Employee@123",
            role="EMPLOYEE",
        )

        # Employee Record
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

    def setUp(self):
        self.client.force_authenticate(user=None)

    def test_admin_can_access_employee_list(self):

        self.client.force_authenticate(
            user=self.admin
        )

        response = self.client.get(
            "/employees/employees/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_hr_can_access_employee_list(self):

        self.client.force_authenticate(
            user=self.hr
        )

        response = self.client.get(
            "/employees/employees/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_unauthenticated_user_denied(self):

        response = self.client.get(
            "/employees/employees/"
        )

        self.assertIn(
            response.status_code,
            [
                status.HTTP_401_UNAUTHORIZED,
                status.HTTP_403_FORBIDDEN,
            ],
        )

    def test_admin_can_view_employee_detail(self):

        self.client.force_authenticate(
            user=self.admin
        )

        response = self.client.get(
            f"/employees/employees/{self.employee.pk}/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_hr_can_view_employee_detail(self):

        self.client.force_authenticate(
            user=self.hr
        )

        response = self.client.get(
            f"/employees/employees/{self.employee.pk}/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_employee_can_view_own_profile(self):

        self.client.force_authenticate(
            user=self.employee_user
        )

        response = self.client.get(
            f"/employees/employees/{self.employee.pk}/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_employee_cannot_access_employee_list(self):

        self.client.force_authenticate(
            user=self.employee_user
        )

        response = self.client.get(
            "/employees/employees/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )