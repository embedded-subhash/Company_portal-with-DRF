from django.db import models

from departments.models import Department
from employees.managers import (
    
    ActiveEmployeeManager,
    HighSalaryManager
)


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
        decimal_places=2,
        db_index=True
    )

    joining_date = models.DateField(
        db_index=True
    )

    designation = models.CharField(
        max_length=100,
        db_index=True
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

    # Custom Managers
    objects = models.Manager()
    active = ActiveEmployeeManager()
    high_salary = HighSalaryManager()

    def __str__(self):

        return (
            f"{self.employee_id} - "
            f"{self.first_name} {self.last_name}"
        )