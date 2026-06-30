import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "company_portal.settings")

app = Celery("company_portal")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()

# 🔥 CELERY BEAT SCHEDULE (AUTOMATION)
app.conf.beat_schedule = {
    
    # DAILY ATTENDANCE REPORT
    "daily-attendance-report": {
        "task": "employees.tasks.report_tasks.generate_attendance_report",
        "schedule": 86400.0,  # 24 hours
    },

    # HOURLY CLEANUP TASK
    "hourly-clean-temp-files": {
        "task": "employees.tasks.report_tasks.cleanup_temp_files",
        "schedule": 3600.0,
    },

    # MONTHLY PAYROLL GENERATION
    "monthly-payroll": {
        "task": "employees.tasks.payroll_tasks.generate_monthly_payroll",
        "schedule": 2592000.0,  # 30 days
    },
}