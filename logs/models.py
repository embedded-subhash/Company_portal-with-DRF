from django.conf import settings
from django.db import models


class SecurityLog(models.Model):
    """
    Audit trail of security-relevant events across the platform.
    Written to by accounts.security.log_event() -- never edited directly by views.
    """

    class Action(models.TextChoices):
        LOGIN_SUCCESS = "LOGIN_SUCCESS", "Login Success"
        LOGIN_FAILURE = "LOGIN_FAILURE", "Login Failure"
        LOGOUT = "LOGOUT", "Logout"
        TOKEN_REFRESH = "TOKEN_REFRESH", "Token Refresh"
        TOKEN_BLACKLISTED = "TOKEN_BLACKLISTED", "Token Blacklisted"
        PASSWORD_CHANGE = "PASSWORD_CHANGE", "Password Change"
        PASSWORD_RESET_REQUESTED = "PASSWORD_RESET_REQUESTED", "Password Reset Requested"
        PASSWORD_RESET_COMPLETED = "PASSWORD_RESET_COMPLETED", "Password Reset Completed"
        UNAUTHORIZED_ACCESS = "UNAUTHORIZED_ACCESS", "Unauthorized Access"
        PERMISSION_DENIED = "PERMISSION_DENIED", "Permission Denied"
        RATE_LIMIT_EXCEEDED = "RATE_LIMIT_EXCEEDED", "Rate Limit Exceeded"
        FILE_UPLOAD_REJECTED = "FILE_UPLOAD_REJECTED", "File Upload Rejected"

    class Status(models.TextChoices):
        SUCCESS = "SUCCESS", "Success"
        FAILURE = "FAILURE", "Failure"
        WARNING = "WARNING", "Warning"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="security_logs",
    )
    actor_identifier = models.CharField(max_length=255, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.CharField(max_length=512, blank=True)
    action = models.CharField(max_length=40, choices=Action.choices)
    status = models.CharField(max_length=10, choices=Status.choices)
    path = models.CharField(max_length=255, blank=True)
    detail = models.CharField(max_length=512, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-timestamp"]
        indexes = [
            models.Index(fields=["action", "-timestamp"]),
            models.Index(fields=["user", "-timestamp"]),
            models.Index(fields=["status", "-timestamp"]),
        ]

    def __str__(self):
        return f"[{self.timestamp:%Y-%m-%d %H:%M:%S}] {self.action} ({self.status}) - {self.actor_identifier or 'anonymous'}"
