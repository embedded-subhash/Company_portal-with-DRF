from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Employee

from .tasks import (
    send_welcome_email,
    notify_hr
)


@receiver(post_save, sender=Employee)
def employee_created_event(sender, instance, created, **kwargs):

    if created:

        print("[SIGNAL] Employee created event triggered")

        # 🔥 CELERY TASKS TRIGGERED AUTOMATICALLY

        send_welcome_email.delay(instance.id)
        notify_hr.delay(instance.id)