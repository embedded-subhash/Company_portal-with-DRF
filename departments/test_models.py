from django.core.exceptions import ValidationError
from django.test import TestCase

from departments.models import Department


class DepartmentModelTests(TestCase):
    def test_department_creation_saves_name_and_description(self):
        department = Department.objects.create(name="Finance", description="Finance operations")
        self.assertEqual(department.name, "Finance")
        self.assertEqual(department.description, "Finance operations")

    def test_duplicate_department_name_is_rejected(self):
        Department.objects.create(name="Sales", description="Sales")
        duplicate = Department(name="Sales", description="Duplicate")
        with self.assertRaises(Exception):
            duplicate.save()

    def test_blank_department_name_is_rejected(self):
        department = Department(name="", description="Missing name")
        with self.assertRaises(ValidationError):
            department.save()

    def test_department_str_representation(self):
        department = Department.objects.create(name="Support", description="Support")
        self.assertEqual(str(department), "Support")
