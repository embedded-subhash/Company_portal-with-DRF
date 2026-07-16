from datetime import date

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from departments.models import Department
from .validators import validate_document_file, validate_image_file


def employee_photo_path(instance, filename):
    return f"employees/{instance.employee_id}/photo/{filename}"


def employee_resume_path(instance, filename):
    return f"employees/{instance.employee_id}/resume/{filename}"


def employee_aadhaar_path(instance, filename):
    return f"employees/{instance.employee_id}/aadhaar/{filename}"


def employee_pan_path(instance, filename):
    return f"employees/{instance.employee_id}/pan/{filename}"
class Employee(models.Model):
    STATUS_CHOICES = (
        ("ACTIVE", "Active"),
        ("INACTIVE", "Inactive"),
    )

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="employee_profile",
        null=True, blank=True,
    )
    employee_id = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, related_name="employees")
    designation = models.CharField(max_length=100)
    salary = models.DecimalField(max_digits=12, decimal_places=2)
    joining_date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="ACTIVE")

    # Module 1: file uploads
    profile_photo = models.ImageField(
        upload_to=employee_photo_path, validators=[validate_image_file], null=True, blank=True
    )
    resume = models.FileField(
        upload_to=employee_resume_path, validators=[validate_document_file], null=True, blank=True
    )
    aadhaar_document = models.FileField(
        upload_to=employee_aadhaar_path, validators=[validate_document_file], null=True, blank=True
    )
    pan_document = models.FileField(
        upload_to=employee_pan_path, validators=[validate_document_file], null=True, blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["employee_id"]

    def __str__(self):
        return f"{self.employee_id} - {self.first_name} {self.last_name}"

    def clean(self):
        super().clean()
        if self.salary is not None and self.salary <= 0:
            raise ValidationError({"salary": "Salary must be a positive number."})
        if self.joining_date and self.joining_date > date.today():
            raise ValidationError({"joining_date": "Joining date cannot be in the future."})

    def save(self, *args, **kwargs):
        self.clean()
        return super().save(*args, **kwargs)

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"


class Attendance(models.Model):
    """Minimal attendance record, used to power attendance reports/dashboard."""

    STATUS_CHOICES = (
        ("PRESENT", "Present"),
        ("ABSENT", "Absent"),
        ("LEAVE", "Leave"),
    )

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="attendance_records")
    date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)

    class Meta:
        unique_together = ("employee", "date")
        ordering = ["-date"]

    def __str__(self):
        return f"{self.employee.employee_id} - {self.date} - {self.status}"
