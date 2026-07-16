from datetime import date

from django.contrib.auth.models import Group
from django.test import TestCase
from rest_framework.test import APIRequestFactory

from accounts.models import User
from departments.models import Department
from employees.models import Employee
from employees.permissions import (
    IsAdmin,
    IsHR,
    IsAdminOrHR,
    IsEmployeeReadOnlySelf,
)


class PermissionTest(TestCase):

    @classmethod
    def setUpTestData(cls):

        cls.factory = APIRequestFactory()

        cls.admin_group = Group.objects.create(name="Admin")
        cls.hr_group = Group.objects.create(name="HR")

        cls.department = Department.objects.create(
            name="IT"
        )

        cls.admin = User.objects.create_user(
            email="admin@test.com",
            password="admin123",
            role="ADMIN"
        )
        cls.admin.groups.add(cls.admin_group)

        cls.hr = User.objects.create_user(
            email="hr@test.com",
            password="hr123",
            role="HR"
        )
        cls.hr.groups.add(cls.hr_group)

        cls.employee_user = User.objects.create_user(
            email="emp@test.com",
            password="emp123",
            role="EMPLOYEE"
        )

        cls.employee = Employee.objects.create(
            user=cls.employee_user,
            employee_id="EMP001",
            first_name="John",
            last_name="Doe",
            email="john@test.com",
            phone="9999999999",
            department=cls.department,
            designation="Developer",
            salary=50000,
            joining_date=date.today(),
        )

    def test_admin_permission(self):

        request = self.factory.get("/")
        request.user = self.admin

        permission = IsAdmin()

        self.assertTrue(
            permission.has_permission(
                request,
                None
            )
        )

    def test_hr_permission(self):

        request = self.factory.get("/")
        request.user = self.hr

        permission = IsHR()

        self.assertTrue(
            permission.has_permission(
                request,
                None
            )
        )

    def test_admin_or_hr_permission(self):

        permission = IsAdminOrHR()

        request = self.factory.get("/")
        request.user = self.admin

        self.assertTrue(
            permission.has_permission(
                request,
                None
            )
        )

        request.user = self.hr

        self.assertTrue(
            permission.has_permission(
                request,
                None
            )
        )

    def test_employee_has_permission(self):

        permission = IsEmployeeReadOnlySelf()

        request = self.factory.get("/")
        request.user = self.employee_user

        self.assertTrue(
            permission.has_permission(
                request,
                None
            )
        )

    def test_employee_object_permission(self):

        permission = IsEmployeeReadOnlySelf()

        request = self.factory.get("/")
        request.user = self.employee_user

        self.assertTrue(
            permission.has_object_permission(
                request,
                None,
                self.employee
            )
        )