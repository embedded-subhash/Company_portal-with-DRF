# Company Portal with Django & PostgreSQL Optimization

## Project Overview

Company Portal is an enterprise-level developed using Django, PostgreSQL, and Django ORM. The project implements production-grade database optimization techniques, transaction management, advanced SQL reporting, and scalable backend architecture.

## Features

### Employee Management

* Employee CRUD Operations
* Employee Search and Filtering
* Department Assignment
* Employee Profile Images
* Role-Based Access Control (RBAC)

### Department Management

* Department CRUD Operations
* One-to-Many Relationship with Employees
* Department-wise Employee Reports

### Payroll Management

* Monthly Payroll Processing
* Salary Management
* Transaction-Based Payroll Operations
* Payroll Reporting

## Database Design

The database follows normalization principles:

* First Normal Form (1NF)
* Second Normal Form (2NF)
* Third Normal Form (3NF)

### Database Relationships

```text
Department
    |
    | One-to-Many
    |
Employee
    |
    | One-to-Many
    |
Payroll
```

## Database Constraints

### Employee Constraints

* Unique Employee ID
* Unique Email Address
* Salary must be greater than or equal to 10000
* Foreign Key constraint on Department

### Department Constraints

* Unique Department Name

Example:

```python
constraints = [
    models.CheckConstraint(
        condition=Q(salary__gte=10000),
        name="salary_greater_than_10000"
    )
]
```

## Database Indexing

Implemented indexes:

* idx_employee_id
* idx_employee_email
* idx_department
* idx_joining_date
* idx_salary
* idx_department_salary

Benefits:

* Faster search operations
* Reduced query execution time
* Improved scalability for large datasets

## Advanced SQL Reports

Implemented reports include:

* Highest Paid Employee
* Lowest Paid Employee
* Top 10 Highest Salaries
* Average Salary by Department
* Employees Joined This Year
* Total Employees per Department
* Departments with More Than 20 Employees
* Employees Earning Above Department Average

## Database Joins

Implemented:

* INNER JOIN
* LEFT JOIN

Examples:

* Employee + Department Report
* Employee + Payroll Report

## Transaction Management

Payroll processing uses Django atomic transactions:

```python
@transaction.atomic
def process_salary():
    pass
```

Features:

* Atomicity
* Consistency
* Isolation
* Durability (ACID)

Rollback occurs automatically if any operation fails.

## Raw SQL Integration

Implemented raw SQL reports using:

```python
from django.db import connection
```

Reports include:

* Top Salary Report
* Department Summary
* Monthly Payroll Report

## ORM Optimization

Implemented:

### select_related()

```python
Employee.objects.select_related("department")
```

### annotate()

```python
Department.objects.annotate(
    total_employees=Count("employee")
)
```

### aggregate()

```python
Employee.objects.aggregate(
    Avg("salary")
)
```

Benefits:

* Eliminates N+1 Query Problem
* Reduces Database Queries
* Improves API Performance

## Database Backup and Restore

### Backup

```bash
pg_dump -U postgres company_db > sql/backup.sql
```

### Restore

```bash
psql -U postgres company_db < sql/backup.sql
```

Automation scripts:

```text
backup_database.bat
restore_database.bat
```

## Project Structure

```text
company_portal/
│
├── employees/
├── departments/
├── payroll/
├── reports/
├── services/
│   └── payroll_service.py
│
├── sql/
│   ├── indexes.sql
│   ├── reports.sql
│   └── backup.sql
│
├── backup_database.bat
├── restore_database.bat
├── QUERY_OPTIMIZATION_REPORT.md
└── README.md
```

## Technology Stack

* Python 3
* Django
* PostgreSQL
* Django ORM
* Raw SQL
* HTML
* Bootstrap
* Git & GitHub

## Git Workflow

```bash
git checkout development

git pull origin development

git checkout -b feature/postgresql-optimization
```

Commit Messages:

```bash
feat: add PostgreSQL constraints

feat: create indexes for employee tables

feat: implement payroll transaction service

feat: optimize ORM queries

feat: add backup and restore scripts
```

## Author

Subhash
Software Engineer | Backend Developer | Django & PostgreSQL Enthusiast
