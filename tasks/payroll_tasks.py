from celery import shared_task
import time


@shared_task(queue="payroll")
def generate_monthly_payroll():

    print("Generating monthly payroll...")

    time.sleep(10)

    print("Payroll generated")

    return {"status": "PAYROLL_DONE"}