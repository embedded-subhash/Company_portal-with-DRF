from celery import shared_task
import time


@shared_task(queue="reports")
def generate_attendance_report():

    print("Generating daily attendance report...")
    time.sleep(5)

    print("Attendance report generated")

    return {"status": "ATTENDANCE_REPORT_DONE"}


@shared_task(queue="reports")
def cleanup_temp_files():

    print("Cleaning temporary files...")
    time.sleep(3)

    print("Cleanup completed")

    return {"status": "CLEANUP_DONE"}