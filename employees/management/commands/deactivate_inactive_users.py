from datetime import timedelta

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone


User = get_user_model()


class Command(BaseCommand):

    help = "Deactivate users inactive for 180 days"

    def handle(self, *args, **kwargs):

        cutoff_date = timezone.now() - timedelta(
            days=180
        )

        users = User.objects.filter(
            last_login__lt=cutoff_date,
            is_active=True
        )

        count = users.count()

        users.update(
            is_active=False
        )

        self.stdout.write(
            self.style.SUCCESS(
                f"{count} users deactivated."
            )
        )