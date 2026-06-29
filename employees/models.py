from django.db import models
from django.db.models import Q, CheckConstraint
from departments.models import Department


class Employee(models.Model):

    employee_id = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)

    salary = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    joining_date = models.DateField()

    designation = models.CharField(max_length=100)

    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE
    )

    profile_image = models.ImageField(
        upload_to='employees/',
        blank=True,
        null=True
    )

    status = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.employee_id} - {self.first_name} {self.last_name}"

    class Meta:

        constraints = [
            CheckConstraint(
                condition=Q(salary__gte=10000),
                name="salary_greater_than_10000"
            ),
        ]

        indexes = [
            models.Index(
                fields=["employee_id"],
                name="idx_employee_id"
            ),

            models.Index(
                fields=["email"],
                name="idx_employee_email"
            ),

            models.Index(
                fields=["department"],
                name="idx_department"
            ),

            models.Index(
                fields=["joining_date"],
                name="idx_joining_date"
            ),

            models.Index(
                fields=["salary"],
                name="idx_salary"
            ),

            models.Index(
                fields=["department", "salary"],
                name="idx_department_salary"
            ),
        ]