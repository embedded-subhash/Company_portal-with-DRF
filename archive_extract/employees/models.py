from datetime import date

from django.conf import settings
from django.core.validators import RegexValidator
from django.db import models

from departments.models import Department


class Skill(models.Model):
    """A skill that can be attached to an employee profile (used in API v2)."""

    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Employee(models.Model):
    """Core employee record."""

    class Status(models.TextChoices):
        ACTIVE = "active", "Active"
        INACTIVE = "inactive", "Inactive"

    employee_id = models.CharField(
        max_length=10,
        unique=True,
        validators=[
            RegexValidator(
                regex=r"^EMP\d{5}$",
                message="Employee ID must be in the format EMP00001 (EMP followed by 5 digits).",
            )
        ],
        help_text="Format: EMP00001",
    )

    # Link to Django's auth user so employees can log in.
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="employee_profile",
        null=True,
        blank=True,
    )

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(
        max_length=10,
        validators=[
            RegexValidator(regex=r"^\d{10}$", message="Phone number must be exactly 10 digits.")
        ],
    )

    department = models.ForeignKey(
        Department, on_delete=models.SET_NULL, null=True, blank=True, related_name="employees"
    )
    designation = models.CharField(max_length=100, blank=True)

    manager = models.ForeignKey(
        "self", on_delete=models.SET_NULL, null=True, blank=True, related_name="team_members"
    )
    skills = models.ManyToManyField(Skill, blank=True, related_name="employees")

    salary = models.DecimalField(max_digits=12, decimal_places=2)
    joining_date = models.DateField()
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.ACTIVE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.employee_id} - {self.first_name} {self.last_name}"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip()

    @property
    def is_active(self):
        return self.status == self.Status.ACTIVE

    @property
    def experience_years(self):
        """Whole years of service since joining_date."""
        today = date.today()
        years = today.year - self.joining_date.year - (
            (today.month, today.day) < (self.joining_date.month, self.joining_date.day)
        )
        return max(years, 0)

    @property
    def annual_salary(self):
        """Salary is stored as monthly salary; annual = monthly * 12."""
        return self.salary * 12
