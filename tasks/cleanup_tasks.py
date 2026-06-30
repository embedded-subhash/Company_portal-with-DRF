from celery import shared_task

@shared_task
def cleanup_inactive_employees():
    print("Cleaning inactive employees")
    return "Cleanup Done"