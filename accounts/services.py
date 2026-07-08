"""
Service-layer helpers kept out of views.py so business logic (token
issuance, email dispatch) is unit-testable independent of HTTP concerns.
"""
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone

from .models import PasswordResetToken


class PasswordResetService:
    @staticmethod
    def issue_token(user):
        """Invalidate any outstanding tokens, then issue a fresh one."""
        PasswordResetToken.objects.filter(user=user, used_at__isnull=True).update(
            used_at=timezone.now()
        )
        return PasswordResetToken.objects.create(user=user)

    @staticmethod
    def send_reset_email(user, token: PasswordResetToken):
        send_mail(
            subject="Company Portal - Password Reset Request",
            message=(
                f"Hello {user.get_full_name() or user.username},\n\n"
                f"Use the following token to reset your password. It expires in "
                f"{PasswordResetToken.EXPIRY_MINUTES} minutes.\n\n"
                f"Reset token: {token.token}\n\n"
                "If you did not request this, you can safely ignore this email."
            ),
            from_email=getattr(settings, "DEFAULT_FROM_EMAIL", "no-reply@company-portal.local"),
            recipient_list=[user.email],
            fail_silently=True,
        )

    @classmethod
    def initiate_reset(cls, user):
        token = cls.issue_token(user)
        cls.send_reset_email(user, token)
        return token
