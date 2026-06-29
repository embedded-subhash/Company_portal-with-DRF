from django.db import models
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
        on_delete=models.CASCADE,
        related_name='employees'
    )

    manager = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='team_members'
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

    def __str__(self):
        return f"{self.employee_id} - {self.first_name} {self.last_name}"
