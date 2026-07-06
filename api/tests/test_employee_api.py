from django.test import TestCase

from api.serializers.employees import EmployeeSerializer
from departments.models import Department
from employees.models import Employee


class EmployeeSerializerValidationTests(TestCase):
    def setUp(self):
        self.department = Department.objects.create(name='Engineering', description='Engineering')

    def test_invalid_employee_id_is_rejected(self):
        data = {
            'employee_id': 'abc',
            'first_name': 'Ajay',
            'last_name': 'Kumar',
            'email': 'ajay@example.com',
            'phone': '9876543210',
            'salary': '50000',
            'joining_date': '2023-01-01',
            'designation': 'Developer',
            'department': self.department.id,
        }
        serializer = EmployeeSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('employee_id', serializer.errors)

    def test_employee_can_be_created_with_current_schema(self):
        data = {
            'employee_id': 'EMP001',
            'first_name': 'Ajay',
            'last_name': 'Kumar',
            'email': 'ajay@example.com',
            'phone': '9876543210',
            'salary': '50000',
            'joining_date': '2023-01-01',
            'designation': 'Developer',
            'department_id': self.department.id,
        }
        serializer = EmployeeSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        employee = serializer.save()
        self.assertTrue(isinstance(employee, Employee))
        self.assertEqual(employee.department, self.department)
