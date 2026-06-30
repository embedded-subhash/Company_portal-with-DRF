from celery import shared_task
import time


@shared_task
def notify_hr(employee_id):

    print(f"Notifying HR about employee {employee_id}")

    time.sleep(3)

    print("HR notified")

    return {
        "employee_id": employee_id,
        "status": "HR Notified"
    }