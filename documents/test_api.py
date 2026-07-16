from datetime import date
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase

from departments.models import Department
from documents.models import EmployeeDocument
from employees.models import Employee

User = get_user_model()


class EmployeeDocumentApiTests(APITestCase):
    def setUp(self):
        self.department = Department.objects.create(name="Legal", description="Legal")
        self.owner = User.objects.create_user(email="owner-doc@example.com", password="StrongPass123!", role="EMPLOYEE")
        self.employee = Employee.objects.create(
            employee_id="EMP00011",
            first_name="Mina",
            last_name="Shah",
            email="mina@example.com",
            phone="9123456780",
            department=self.department,
            designation="Counsel",
            salary=Decimal("170000.00"),
            joining_date=date(2024, 3, 1),
            user=self.owner,
        )
        self.other_user = User.objects.create_user(email="other-doc@example.com", password="StrongPass123!", role="EMPLOYEE")

    def test_list_documents_requires_authentication(self):
        response = self.client.get("/api/v1/documents/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_owner_can_create_and_list_documents(self):
        self.client.force_authenticate(self.owner)
        file = SimpleUploadedFile("resume.pdf", b"%PDF-1.4 test", content_type="application/pdf")
        response = self.client.post(
            "/api/v1/documents/",
            {
                "employee": self.employee.id,
                "document_name": "Resume",
                "document_type": "RESUME",
                "file": file,
            },
            format="multipart",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(EmployeeDocument.objects.count(), 1)

        list_response = self.client.get("/api/v1/documents/")
        self.assertEqual(list_response.status_code, status.HTTP_200_OK)

    def test_other_user_cannot_access_another_employee_document(self):
        document = EmployeeDocument.objects.create(
            employee=self.employee,
            document_name="Resume",
            document_type="RESUME",
            file=SimpleUploadedFile("resume.pdf", b"%PDF-1.4 test", content_type="application/pdf"),
            uploaded_by=self.owner,
        )
        self.client.force_authenticate(self.other_user)
        response = self.client.get(f"/api/v1/documents/{document.id}/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_download_endpoint_returns_file_for_owner(self):
        document = EmployeeDocument.objects.create(
            employee=self.employee,
            document_name="Resume",
            document_type="RESUME",
            file=SimpleUploadedFile("resume.pdf", b"%PDF-1.4 test", content_type="application/pdf"),
            uploaded_by=self.owner,
        )
        self.client.force_authenticate(self.owner)
        response = self.client.get(f"/api/v1/documents/{document.id}/download/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
