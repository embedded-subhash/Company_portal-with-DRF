from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone

from departments.models import Department


class Employee(models.Model):

    employee_id = models.CharField(
        max_length=20,
        unique=True
    )

    first_name = models.CharField(
        max_length=100
    )

    last_name = models.CharField(
        max_length=100
    )

    email = models.EmailField(
        unique=True
    )

    phone = models.CharField(
        max_length=15
    )

    salary = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    joining_date = models.DateField()

    designation = models.CharField(
        max_length=100
    )

    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE
    )

    profile_image = models.ImageField(
        upload_to='employees/',
        blank=True,
        null=True
    )

    # True = Active
    # False = Inactive
    status = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def clean(self):

        if self.salary < 0:

            raise ValidationError({
                "salary": "Salary cannot be negative."
            })

        if self.joining_date > timezone.now().date():

            raise ValidationError({
                "joining_date":
                "Joining date cannot be in the future."
            })

    def save(self, *args, **kwargs):

        self.full_clean()

        if self.pk:

            old_employee = Employee.objects.get(
                pk=self.pk
            )

            if old_employee.employee_id != self.employee_id:

                raise ValidationError(
                    "Employee ID cannot be changed."
                )

        super().save(*args, **kwargs)

    def __str__(self):

        return (
            f"{self.employee_id} - "
            f"{self.first_name} {self.last_name}"
        )


class EmployeeProfile(models.Model):

    employee = models.OneToOneField(
        Employee,
        on_delete=models.CASCADE,
        related_name='profile'
    )

    address = models.TextField(
        blank=True
    )

    emergency_contact = models.CharField(
        max_length=15,
        blank=True
    )

    blood_group = models.CharField(
        max_length=5,
        blank=True
    )

    photo = models.ImageField(
        upload_to='employee_profiles/',
        blank=True,
        null=True
    )

    skills = models.TextField(
        blank=True
    )

    bio = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):

        return (
            f"Profile - "
            f"{self.employee.first_name} "
            f"{self.employee.last_name}"
        )


class BlockedIP(models.Model):

    ip_address = models.GenericIPAddressField(
        unique=True
    )

    reason = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return self.ip_address

class ArchivedEmployee(models.Model):

    employee_id = models.CharField(
        max_length=20
    )

    first_name = models.CharField(
        max_length=100
    )

    last_name = models.CharField(
        max_length=100
    )

    email = models.EmailField()

    department_name = models.CharField(
        max_length=100
    )

    salary = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    deleted_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return self.employee_id