import uuid

from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import BaseUserManager
from django.utils import timezone


class UserManager(BaseUserManager):

    def _generate_employee_id(self):
        existing_ids = set(
            self.model.objects.values_list('employee_id', flat=True)
        )
        counter = 1
        while True:
            candidate = f'EMP{counter:05d}'
            if candidate not in existing_ids:
                return candidate
            counter += 1

    def create_user(self, email, password=None, **extra_fields):

        if not email:
            raise ValueError("Email is required")

        email = self.normalize_email(email)

        extra_fields.setdefault('employee_id', self._generate_employee_id())
        extra_fields.setdefault('phone', '0000000000')
        extra_fields.setdefault('role', 'EMPLOYEE')

        user = self.model(
            email=email,
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password=None, **extra_fields):

        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('phone', '0000000000')
        extra_fields.setdefault('role', 'ADMIN')

        return self.create_user(
            email=email,
            password=password,
            **extra_fields
        )


class PasswordResetToken(models.Model):
    EXPIRY_MINUTES = 15

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="password_reset_tokens",
    )
    token = models.CharField(max_length=64, unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    used_at = models.DateTimeField(null=True, blank=True)

    def is_valid(self):
        if self.used_at is not None:
            return False
        return timezone.now() < self.created_at + timezone.timedelta(minutes=self.EXPIRY_MINUTES)

    def save(self, *args, **kwargs):
        if not self.token:
            self.token = uuid.uuid4().hex
        return super().save(*args, **kwargs)

    def mark_used(self):
        self.used_at = timezone.now()
        self.save(update_fields=["used_at"])


class User(AbstractUser):

    ROLE_CHOICES = [
        ('ADMIN', 'Admin'),
        ('HR', 'HR'),
        ('MANAGER', 'Manager'),
        ('EMPLOYEE', 'Employee'),
    ]

    username = None

    email = models.EmailField(
        unique=True
    )

    employee_id = models.CharField(
        max_length=20,
        unique=True
    )

    phone = models.CharField(
        max_length=15
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='EMPLOYEE'
    )

    profile_image = models.ImageField(
        upload_to='profile_images/',
        blank=True,
        null=True
    )

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return f"{self.email} - {self.role}"