#  — Django Signals, Middleware & Custom Management Commands (HRMS Automation Module)

## Project Overview

This module implements enterprise-level backend automation using Django Signals, Middleware, Custom Management Commands, Logging, and Audit Trail systems. These features are essential in real-world HRMS, ERP, Banking, and Enterprise SaaS applications where system-level automation, monitoring, and security are critical.

The system focuses on automating employee lifecycle events, tracking system activity, enforcing security policies, and generating analytical reports.

---

## Training Goal

Learn how to implement Django Signals, Middleware, Custom Management Commands, Logging systems, and Audit Trails to build scalable enterprise backend systems with automation and observability.

---

## Company Scenario (Real-world HRMS Requirements)

The HRMS system must support:

* Automatic EmployeeProfile creation when Employee is created
* Audit logging for all CRUD operations
* Login and logout tracking
* Request performance monitoring
* IP-based access restriction
* Automated report generation using Django commands
* System-wide logging and error tracking

---

# Module 1: Django Signals

## Signal Types

* `pre_save`
* `post_save`
* `pre_delete`
* `post_delete`
* `m2m_changed`

---

## Signal Flow

```text id="sig01"
Employee Created
      ↓
post_save Signal Triggered
      ↓
Create EmployeeProfile
      ↓
Write Audit Log
      ↓
Send Notification (optional)
```

---

## Practical Task 1: Employee Signals Automation

### Requirements

When Employee is created:

* Create EmployeeProfile automatically
* Create Audit Log entry
* Record joining date

When Employee is updated:

* Store previous salary
* Store previous department
* Log update action

When Employee is deleted:

* Archive employee data
* Create deletion log

---

# Module 2: Employee Profile Automation

## Models Relationship

* Employee → EmployeeProfile (One-to-One)

---

## EmployeeProfile Fields

* Employee (FK/OneToOne)
* Address
* Emergency Contact
* Blood Group
* Photo
* Skills
* Bio

---

## Practical Task 2

Automatically create EmployeeProfile whenever a new Employee is added using signals.

---

# Module 3: Audit Logging System

## AuditLog Model

Fields:

* id
* user
* action
* module
* object_id
* timestamp
* ip_address
* request_method

---

## Practical Task 3

Log the following events:

* Employee Created
* Employee Updated
* Employee Deleted
* Department Created
* User Login
* User Logout

---

# Module 4: Django Middleware

## What is Middleware?

Middleware processes requests before reaching the view and processes responses before sending them back to the client.

---

## Request Flow

```text id="mw01"
Request → Middleware → View → Middleware → Response
```

---

## Practical Task 4: Custom Middleware Implementation

### 1. Request Logging Middleware

Logs:

* URL
* HTTP Method
* IP Address
* User
* Response Time

Stored in:

```text id="log01"
logs/request.log
```

---

### 2. Response Time Middleware

Tracks:

* Start time
* End time
* Total response time

If response time > 500ms:

* Log warning

---

### 3. IP Restriction Middleware

## BlockedIP Model

* ip_address
* reason
* created_at

---

### Behavior

If request comes from blocked IP:

* Return `403 Forbidden`

---

# Module 5: Custom Management Commands

## Command Structure

```text id="cmd01"
employees/
└── management/
    └── commands/
        ├── generate_reports.py
        ├── seed_data.py
        └── deactivate_inactive_users.py
```

---

## Practical Task 5

### Command 1: Generate Reports

```bash id="cmd02"
python manage.py generate_reports
```

Generates:

* Employee Summary
* Department Summary
* Salary Summary

Saved in:

```text id="rep01"
reports/
```

---

### Command 2: Deactivate Inactive Users

```bash id="cmd03"
python manage.py deactivate_inactive_users
```

Requirements:

* Identify users inactive for 180+ days
* Mark them inactive
* Generate report

---

### Command 3: Seed Data

```bash id="cmd04"
python manage.py seed_data
```

Generates:

* 10 Departments
* 100 Employees
* 20 Managers

---

# Module 6: Django Logging System

## Logging Files

```text id="log02"
logs/
├── application.log
├── error.log
└── security.log
```

---

## Log Categories

### INFO

* Employee Created

### WARNING

* Slow response detected

### ERROR

* Database failure

### SECURITY

* Unauthorized access attempt

---

# Module 7: Exception Handling

## Custom Error Pages

Create templates:

```text id="err01"
404.html
403.html
500.html
```

---

## Error Page Features

* Error Code display
* Friendly message
* Navigation to dashboard

---

# Module 8: Admin Panel Enhancements

## EmployeeAdmin Features

* Search functionality
* Filters
* Date hierarchy
* Read-only fields
* Bulk actions

---

## Bulk Actions

* Activate Employees
* Deactivate Employees
* Export selected employees to CSV

---

## Practical Task 8

Implement:

* CSV Export action
* Bulk activation/deactivation

---

# Module 9: HRMS Dashboard Analytics

## Dashboard Metrics

* Total Employees
* Active Employees
* Departments
* Employees Joined Today
* Employees Joined This Month
* Inactive Users
* Salary Distribution

---

# Module 10: Data Validation

## Model Validation

### Rules

* Salary cannot be negative
* Joining date cannot be in the future
* Employee ID cannot be modified after creation

---

## Implementation Points

### clean()

Used for model-level validation

### save()

Used to enforce business logic before saving

---

# Professional Project Structure

```text id="proj01"
company_portal/
│
├── employees/
│   ├── models.py
│   ├── signals.py
│   ├── middleware.py
│   ├── admin.py
│   ├── validators.py
│   │
│   └── management/
│       └── commands/
│           ├── generate_reports.py
│           ├── seed_data.py
│           └── deactivate_inactive_users.py
│
├── audit_logs/
├── reports/
├── logs/
└── templates/
    ├── 403.html
    ├── 404.html
    └── 500.html
```

---

# Company-Level Assignment

## HRMS Automation Module

### Features to Implement

* Employee Profile Auto Creation (Signals)
* Audit Logging System
* Request Logging Middleware
* Response Time Middleware
* IP Blocking Middleware
* Report Generation Commands
* Seed Data Generation
* Logging System (multi-file)
* Custom Error Pages
* Admin Bulk Actions

---

# Git Workflow

```bash id="git01"
git checkout development
git pull origin development
git checkout -b feature/django-signals-middleware
```

---

## Commit Standards

* feat: implement Django signals automation
* feat: add audit logging system
* feat: implement custom middleware
* feat: add management commands
* feat: implement HRMS automation layer

---

# Jira Story

## Story Title

HRMS Automation Module — Signals, Middleware & Management Commands

---

## Description

As a Django Backend Developer Trainee,

I need to implement Django Signals, Middleware, Custom Management Commands, Logging, and Audit Systems so that the HRMS application supports automation, monitoring, and enterprise-grade backend architecture.

---

# Acceptance Criteria

* Employee Profile auto creation implemented using signals
* Audit logging system implemented
* Request logging middleware implemented
* Response time middleware implemented
* IP blocking middleware implemented
* Custom management commands implemented
* Logging system with multiple log files implemented
* Custom error pages implemented
* Admin bulk actions implemented
* Git feature branch workflow followed


After completing this module, developers will understand:

* Django Signals lifecycle automation
* Middleware request/response processing
* Custom management command creation
* Enterprise logging strategies
* Audit trail implementation
* System monitoring techniques
* Security enforcement using IP blocking
* Production-level Django architecture

---

# Author

**Subhash**

Software Engineer | Django Backend Developer | HRMS Automation & Enterprise Architecture Learner
