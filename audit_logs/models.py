from django.db import models
from django.conf import settings


class AuditLog(models.Model):

    ACTION_CHOICES = [
        ('CREATE', 'Create'),
        ('UPDATE', 'Update'),
        ('DELETE', 'Delete'),
        ('LOGIN', 'Login'),
        ('LOGOUT', 'Logout'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    action = models.CharField(
        max_length=20,
        choices=ACTION_CHOICES
    )

    module = models.CharField(
        max_length=100
    )

    object_id = models.IntegerField(
        null=True,
        blank=True
    )

    timestamp = models.DateTimeField(
        auto_now_add=True
    )

    ip_address = models.GenericIPAddressField(
        null=True,
        blank=True
    )

    request_method = models.CharField(
        max_length=10,
        blank=True
    )

    def __str__(self):
        return f"{self.action} - {self.module}"