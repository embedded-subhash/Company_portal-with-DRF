from django.conf import settings
from django.db import models


class UserProfile(models.Model):
    """Extra role information attached to Django's built-in User model.

    Role drives the custom permission classes in api/permissions/.
    """

    class Role(models.TextChoices):
        ADMIN = "admin", "Admin"
        HR = "hr", "HR"
        EMPLOYEE = "employee", "Employee"

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile"
    )
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.EMPLOYEE)

    def __str__(self):
        return f"{self.user.username} ({self.role})"
