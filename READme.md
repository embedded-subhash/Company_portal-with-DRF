# Django HR Management System

A professional Employee Management Portal built using Django and PostgreSQL. This application provides employee registration, profile management, CRUD operations, form validation, image upload support, search, filtering, and pagination.

## Features

### Employee Management

* Create Employee
* View Employee List
* View Employee Details
* Update Employee Information
* Delete Employee Records

### Department Management

* Department Creation
* Department Assignment to Employees

### Form Validation

* Employee ID Validation (EMP001 Format)
* Unique Employee ID
* Unique Email Validation
* Phone Number Validation
* Salary Range Validation
* Joining Date Validation

### Profile Image Upload

* Upload Employee Profile Image
* Display Employee Image
* Update Employee Image

### Search and Filtering

* Search by Employee ID
* Search by Name
* Search by Email
* Filter by Department
* Filter by Status

### Pagination

* 10 Employees Per Page

### Django Generic Views

* CreateView
* ListView
* DetailView
* UpdateView
* DeleteView

### Messages Framework

* Success Messages
* Error Messages
* Validation Messages

---

## Technology Stack

* Python 3.14
* Django 6
* PostgreSQL
* HTML
* CSS
* Bootstrap (Optional)
* Pillow

---

## Project Structure

company_portal/

├── company_portal/

├── employees/

│   ├── forms.py

│   ├── models.py

│   ├── views.py

│   ├── urls.py

│   └── templates/

│       └── employees/

├── departments/

│   ├── models.py

│   └── admin.py

├── media/

│   └── employees/

├── manage.py

└── requirements.txt

---

## Installation

### Clone Repository

```bash
git clone https://github.com/embedded-subhash/django-hr-management-system.git

cd django-hr-management-system
```

### Create Virtual Environment

```bash
python -m venv .venv
```

### Activate Virtual Environment

Windows

```bash
.venv\Scripts\activate
```

Linux/Mac

```bash
source .venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## PostgreSQL Configuration

Create Database

```sql
CREATE DATABASE company_db;
```

Update settings.py

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'company_db',
        'USER': 'postgres',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

---

## Run Migrations

```bash
python manage.py makemigrations

python manage.py migrate
```

---

## Create Superuser

```bash
python manage.py createsuperuser
```

---

## Run Server

```bash
python manage.py runserver
```

Open:

```text
http://127.0.0.1:8000/
```

Employee Module:

```text
http://127.0.0.1:8000/employees/
```

Admin Panel:

```text
http://127.0.0.1:8000/admin/
```

---

## Employee CRUD URLs

| Function        | URL                     |
| --------------- | ----------------------- |
| Employee List   | /employees/             |
| Create Employee | /employees/create/      |
| Employee Detail | /employees/<id>/        |
| Update Employee | /employees/update/<id>/ |
| Delete Employee | /employees/delete/<id>/ |

---

## Screenshots

Include:

* Employee List
* Create Employee
* Employee Detail
* Update Employee
* Delete Employee
* Validation Errors
* Search and Filter
* Profile Image Upload

---

## Git Workflow

```bash
git checkout development

git pull origin development

git checkout -b feature/employee-crud
```

Commit Messages

```bash
feat: implement employee forms

feat: implement CRUD operations

feat: add profile image upload

feat: implement search and filtering

feat: add pagination support
```

---

## Author

Subhash

Software Engineer

Django Backend Developer Trainee

---

## Project Status

Completed

* Employee Registration
* CRUD Operations
* PostgreSQL Integration
* Form Validation
* Django Generic Views
* Profile Image Upload
* Pagination
* Messages Framework
