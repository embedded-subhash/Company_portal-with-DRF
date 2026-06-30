from celery import shared_task
import time


@shared_task
def generate_attendance_report():

    print("Generating attendance report")

    time.sleep(8)

    print("Attendance report generated")

    return {
        "status": "Attendance Report Generated"
    }