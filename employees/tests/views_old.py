from datetime import date

from django.contrib.auth.models import Group
from django.test import TestCase
from django.urls import reverse

from accounts.models import User
from departments.models import Department
from employees.models import Employee


class EmployeeViewsTest(TestCase):

    @classmethod
    def setUpTestData(cls):

        admin_group = Group.objects.create(name="Admin")

        cls.user = User.objects.create_user(
            email="admin@test.com",
            password="admin123",
            role="ADMIN"
        )

        cls.user.groups.add(admin_group)

        cls.department = Department.objects.create(
            name="IT"
        )

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
        self.client.force_login(self.user)

    def test_employee_list_view(self):

        response = self.client.get(
            reverse("employee_list")
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            "employees/list.html"
        )
        self.assertContains(
            response,
            "John"
        )

    def test_employee_detail_view(self):

        response = self.client.get(
            reverse(
                "employee_detail",
                args=[self.employee.pk]
            )
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            "employees/detail.html"
        )

    def test_employee_create_view_get(self):

        response = self.client.get(
            reverse("employee_create")
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            "employees/create.html"
        )

    def test_employee_create_view_post(self):

        response = self.client.post(
            reverse("employee_create"),
            {
                "employee_id": "EMP002",
                "first_name": "Subhash",
                "last_name": "Kumar",
                "email": "subhash@test.com",
                "phone": "9999999999",
                "department": self.department.id,
                "designation": "Python Developer",
                "salary": 60000,
                "joining_date": date.today(),
                "status": "ACTIVE",
            }
        )

        self.assertEqual(response.status_code, 302)

        self.assertTrue(
            Employee.objects.filter(
                employee_id="EMP002"
            ).exists()
        )

    def test_employee_update_view(self):

        response = self.client.post(
            reverse(
                "employee_update",
                args=[self.employee.pk]
            ),
            {
                "employee_id": "EMP001",
                "first_name": "John",
                "last_name": "Doe",
                "email": "john@test.com",
                "phone": "9876543210",
                "department": self.department.id,
                "designation": "Senior Developer",
                "salary": 70000,
                "joining_date": date.today(),
                "status": "ACTIVE",
            }
        )

        self.assertEqual(response.status_code, 302)

        self.employee.refresh_from_db()

        self.assertEqual(
            self.employee.designation,
            "Senior Developer"
        )

    def test_employee_delete_view(self):

        response = self.client.post(
            reverse(
                "employee_delete",
                args=[self.employee.pk]
            )
        )

        self.assertEqual(response.status_code, 302)

        self.assertFalse(
            Employee.objects.filter(
                pk=self.employee.pk
            ).exists()
        )