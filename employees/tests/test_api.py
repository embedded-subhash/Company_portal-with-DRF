from datetime import date

from django.contrib.auth.models import Group
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from accounts.models import User
from departments.models import Department
from employees.models import Employee


class EmployeeAPITest(APITestCase):

    @classmethod
    def setUpTestData(cls):

        admin_group = Group.objects.create(name="Admin")

        cls.department = Department.objects.create(
            name="IT"
        )

        cls.admin = User.objects.create_user(
            email="admin@test.com",
            password="admin123",
            role="ADMIN",
        )

        cls.admin.groups.add(admin_group)

        cls.employee = Employee.objects.create(
            employee_id="EMP001",
            first_name="John",
            last_name="Doe",
            email="john@test.com",
            phone="9876543210",
            department=cls.department,
            designation="Developer",
            salary=50000,
            joining_date=date.today(),
            status="ACTIVE",
        )

    def setUp(self):

        response = self.client.post(
            reverse("api-login"),
            {
                "email": "admin@test.com",
                "password": "admin123",
            },
            format="json",
        )

        token = response.data["access"]

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {token}"
        )

    def test_employee_list(self):

        response = self.client.get(
            "/api/v1/employees/employees/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

    def test_employee_create(self):

        response = self.client.post(
            "/api/v1/employees/employees/",
            {
                "employee_id": "EMP002",
                "first_name": "Subhash",
                "last_name": "Kumar",
                "email": "subhash@test.com",
                "phone": "9999999999",
                "department": self.department.id,
                "designation": "Python Developer",
                "salary": 60000,
                "joining_date": str(date.today()),
                "status": "ACTIVE",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

    def test_employee_detail(self):

        response = self.client.get(
            f"/api/v1/employees/employees/{self.employee.id}/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

    def test_employee_update(self):

        response = self.client.patch(
            f"/api/v1/employees/employees/{self.employee.id}/",
            {
                "designation": "Senior Developer"
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

    def test_employee_delete(self):

        response = self.client.delete(
            f"/api/v1/employees/employees/{self.employee.id}/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
        )

    def test_unauthorized_access(self):

        self.client.credentials()

        response = self.client.get(
            "/api/v1/employees/employees/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )