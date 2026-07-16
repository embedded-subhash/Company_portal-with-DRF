from django.test import TestCase
from unittest.mock import patch
from datetime import date

from employees.models import Employee
from employees.services.email_service import send_employee_email


class EmailServiceTest(TestCase):

    def setUp(self):

        self.employee = Employee.objects.create(
            employee_id="EMP001",
            first_name="Subhash",
            last_name="Test",
            email="test@gmail.com",
            phone="9999999999",
            salary=50000,
            joining_date=date.today(),
            designation="Software Engineer"
        )


    @patch("employees.services.email_service.send_mail")
    def test_send_employee_email(self, mock_send):

        send_employee_email(self.employee)

        mock_send.assert_called_once()

        mock_send.assert_called_once_with(
    subject="Welcome",
    message="Welcome Employee",
    from_email="hr@company.com",
    recipient_list=["test@gmail.com"]
)