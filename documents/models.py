from django.conf import settings
from django.db import models

from employees.models import Employee
from employees.validators import validate_document_file, validate_image_file

DOCUMENT_TYPE_CHOICES = (
    ("RESUME", "Resume"),
    ("AADHAAR", "Aadhaar"),
    ("PAN", "PAN"),
    ("DEGREE_CERTIFICATE", "Degree Certificate"),
    ("EXPERIENCE_CERTIFICATE", "Experience Certificate"),
    ("OFFER_LETTER", "Offer Letter"),
    ("OTHER", "Other"),
)

# Documents that must be images vs must be PDFs
IMAGE_DOCUMENT_TYPES = set()  # currently none - photo lives on Employee.profile_photo


def employee_document_path(instance, filename):
    return f"documents/{instance.employee.employee_id}/{instance.document_type.lower()}/{filename}"


class EmployeeDocument(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="documents")
    document_name = models.CharField(max_length=150)
    document_type = models.CharField(max_length=30, choices=DOCUMENT_TYPE_CHOICES)
    file = models.FileField(upload_to=employee_document_path, validators=[validate_document_file])
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="uploaded_documents"
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-uploaded_at"]

    def __str__(self):
        return f"{self.employee.employee_id} - {self.document_name}"
