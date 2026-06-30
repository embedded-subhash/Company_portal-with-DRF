# Company Portal - Enterprise Background Job Processing System

## Training Goal

This project implements enterprise-grade asynchronous processing using Celery, Redis, and Django to handle long-running operations without blocking user requests.

---

## Features Implemented

### Background Tasks

- Welcome Email Queue
- Salary PDF Generation
- Salary Email Sending
- HR Notifications
- Attendance Report Generation

### Celery Features

- Celery + Redis Integration
- Django Celery Results
- Celery Beat Scheduler
- Multiple Queues
- Task Status API
- Logging
- Flower Monitoring

### Employee Features

- Employee CRUD Operations
- Excel Bulk Import
- Welcome Email Queue After Import
- PostgreSQL Database Integration

---

## Technology Stack

- Python 3.14
- Django 6.0
- PostgreSQL
- Celery 5.6
- Redis
- Flower
- OpenPyXL

---

## Installation

### Clone Repository

```bash
git clone <your-repository-url>
cd company_portal
```

### Create Virtual Environment

```bash
python -m venv .venv
```

Activate:

```bash
.venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Database Configuration

Update:

```python
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "company_db",
        "USER": "postgres",
        "PASSWORD": "********",
        "HOST": "localhost",
        "PORT": "5432",
    }
}
```

Apply migrations:

```bash
python manage.py migrate
```

---

## Redis Setup

Start Redis:

```bash
redis-server
```

Verify:

```bash
redis-cli ping
```

Expected:

```text
PONG
```

---

## Celery Configuration

Broker:

```python
CELERY_BROKER_URL = "redis://localhost:6379/0"
```

Result Backend:

```python
CELERY_RESULT_BACKEND = "django-db"
```

---

## Running Celery Workers

### Email Worker

```bash
celery -A company_portal worker -Q emails -l info
```

### Payroll Worker

```bash
celery -A company_portal worker -Q payroll -l info
```

### Reports Worker

```bash
celery -A company_portal worker -Q reports -l info
```

### Notification Worker

```bash
celery -A company_portal worker -Q notifications -l info
```

---

## Running Celery Beat

```bash
celery -A company_portal beat -l info
```

---

## Running Flower

Install:

```bash
pip install flower
```

Run:

```bash
celery -A company_portal flower
```

Dashboard:

```text
http://localhost:5555
```

---

## Available Queues

| Queue | Purpose |
|---------|----------|
| emails | Welcome emails and salary emails |
| payroll | Salary PDF generation |
| reports | Attendance reports |
| notifications | HR notifications |

---

## Background Tasks

### Welcome Email

```python
send_welcome_email(employee_id)
```

### Salary PDF

```python
generate_salary_pdf(employee_id)
```

### Salary Email

```python
send_salary_email(employee_id)
```

### HR Notification

```python
notify_hr(employee_id)
```

### Attendance Report

```python
generate_attendance_report()
```

---

## Task Status API

Endpoint:

```text
GET /employees/tasks/<task_id>/
```

Response:

```json
{
    "task_id": "123abc",
    "status": "SUCCESS",
    "result": {
        "employee_id": 101,
        "status": "SUCCESS"
    }
}
```

---

## Scheduled Tasks

### Daily Attendance Report

```text
6:00 PM Daily
```

### Monthly Payroll Generation

```text
1st Day of Month - 2:00 AM
```

### Weekly HR Notification

```text
Monday - 9:00 AM
```

### Hourly Cleanup

```text
Every Hour
```

---

## Excel Bulk Import

Features:

- Upload Excel File
- Save Employees
- Queue Welcome Emails
- Generate Import Summary

Endpoint:

```text
/employees/import/
```

---

## Logs

Log file:

```text
logs/celery.log
```

---

## Git Workflow

```bash
git checkout development

git pull origin development

git checkout -b feature/celery-background-jobs
```

Commit Messages:

```bash
feat: configure Celery and Redis

feat: implement asynchronous email queue

feat: add payroll background processing

feat: configure Celery Beat scheduler

feat: integrate Flower monitoring
```

---

## Project Structure

```text
company_portal/
│
├── company_portal/
│   ├── celery.py
│   └── settings.py
│
├── employees/
│   ├── tasks.py
│   ├── services/
│   ├── forms/
│   ├── views/
│   └── templates/
│
├── media/
├── logs/
│
└── manage.py
```

---

## Screenshots

Add:

- Flower Dashboard Screenshot
- Celery Worker Screenshot
- Celery Beat Screenshot
- Background Task Logs
- Excel Import Screenshot

---

## Author

Subhash

Software Engineer | Backend & Embedded Systems Developer