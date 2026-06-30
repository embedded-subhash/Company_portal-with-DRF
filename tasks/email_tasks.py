from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
import time
import logging
import random

logger = logging.getLogger(__name__)


# =====================================================
# 1. WELCOME EMAIL TASK
# =====================================================

@shared_task(
    bind=True,
    max_retries=5,
    default_retry_delay=30,
    queue="emails"
)
def send_welcome_email(self, employee_id, email):

    try:

        logger.info(
            f"Sending welcome email to Employee {employee_id}"
        )

        time.sleep(3)

        # Simulate email server failure
        if random.randint(1, 3) == 1:
            raise Exception("SMTP Server Temporarily Unavailable")

        send_mail(
            subject="Welcome to HRMS",
            message=f"Hello Employee {employee_id}, welcome to the company.",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            fail_silently=False,
        )

        logger.info(
            f"Welcome email sent to Employee {employee_id}"
        )

        return {
            "employee_id": employee_id,
            "status": "WELCOME_EMAIL_SENT"
        }

    except Exception as exc:

        logger.error(
            f"Welcome email failed for {employee_id}: {exc}"
        )

        raise self.retry(exc=exc)


# =====================================================
# 2. SALARY EMAIL TASK
# =====================================================

@shared_task(
    bind=True,
    max_retries=5,
    default_retry_delay=30,
    queue="emails"
)
def send_salary_email(self, employee_id, email, file_path=None):

    try:

        logger.info(
            f"Sending salary email for Employee {employee_id}"
        )

        time.sleep(3)

        # Simulate temporary failure
        if random.randint(1, 4) == 1:
            raise Exception("Mail Server Busy")

        send_mail(
            subject="Your Salary Slip",
            message=(
                f"Hello Employee {employee_id}, "
                f"please find your salary slip."
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            fail_silently=False,
        )

        logger.info(
            f"Salary email sent for Employee {employee_id}"
        )

        return {
            "employee_id": employee_id,
            "file_path": file_path,
            "status": "SALARY_EMAIL_SENT"
        }

    except Exception as exc:

        logger.error(
            f"Salary email failed for {employee_id}: {exc}"
        )

        raise self.retry(exc=exc)


# =====================================================
# 3. HR NOTIFICATION TASK
# =====================================================

@shared_task(
    bind=True,
    max_retries=5,
    default_retry_delay=20,
    queue="notifications"
)
def notify_hr(self, employee_id):

    try:

        logger.info(
            f"Notifying HR for Employee {employee_id}"
        )

        time.sleep(2)

        # Simulate notification service failure
        if random.randint(1, 4) == 1:
            raise Exception("Notification Service Down")

        send_mail(
            subject="New Employee Joined",
            message=(
                f"Employee {employee_id} "
                f"has joined the organization."
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=["hr@company.com"],
            fail_silently=False,
        )

        logger.info(
            f"HR notified for Employee {employee_id}"
        )

        return {
            "employee_id": employee_id,
            "status": "HR_NOTIFIED"
        }

    except Exception as exc:

        logger.error(
            f"HR notification failed for {employee_id}: {exc}"
        )

        raise self.retry(exc=exc)