from celery import shared_task
import time


# =========================
# EMAIL QUEUE
# =========================

@shared_task(queue="emails")
def send_welcome_email(employee_id):

    print(f"Sending welcome email to employee {employee_id}")

    time.sleep(5)

    print("Welcome email sent")

    return {
        "employee_id": employee_id,
        "status": "SUCCESS"
    }


@shared_task(queue="emails")
def send_salary_email(employee_id):

    print(f"Sending salary email to employee {employee_id}")

    time.sleep(5)

    print("Salary email sent")

    return {
        "employee_id": employee_id,
        "status": "SALARY_EMAIL_SENT"
    }


# =========================
# PAYROLL QUEUE
# =========================

@shared_task(queue="payroll")
def generate_salary_pdf(employee_id):

    print(f"Generating salary PDF for employee {employee_id}")

    time.sleep(10)

    print("Salary PDF generated")

    return {
        "employee_id": employee_id,
        "status": "PDF_GENERATED"
    }


# =========================
# NOTIFICATION QUEUE
# =========================

@shared_task(queue="notifications")
def notify_hr(employee_id):

    print(f"Notifying HR about employee {employee_id}")

    time.sleep(3)

    print("HR notified")

    return {
        "employee_id": employee_id,
        "status": "HR_NOTIFIED"
    }


# =========================
# REPORTS QUEUE
# =========================

@shared_task(queue="reports")
def generate_attendance_report():

    print("Generating attendance report")

    time.sleep(8)

    print("Attendance report generated")

    return {
        "status": "ATTENDANCE_REPORT_GENERATED"
    }


# =========================
# CLEANUP TASK (Celery Beat)
# =========================

@shared_task(queue="reports")
def cleanup_temp_data():

    print("Cleaning temporary files...")

    time.sleep(2)

    print("Temporary files cleaned")

    return {
        "status": "TEMP_FILES_CLEANED"
    }