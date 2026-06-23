# Django HR Management System

## Overview

Django HR Management System is a professional Employee Management Portal developed using Django and PostgreSQL. The application provides role-based access control, employee management, department management, authentication, authorization, dashboard analytics, password management, and profile management.

---

## Features

### Authentication & Authorization

* Custom User Model
* Email-based Authentication
* User Registration
* Login & Logout
* Role-Based Access Control (RBAC)
* Dynamic Permission Assignment

### User Roles

* Admin
* HR
* Manager
* Employee

### Employee Management

* Create Employee
* View Employee
* Update Employee
* Delete Employee
* Search Employees
* Employee Status Management
* Pagination Support

### Department Management

* Create Department
* Update Department
* Delete Department
* Department Listing

### Dashboards

#### Admin Dashboard

* Total Users
* Total Employees
* Total Departments
* Active Users

#### HR Dashboard

* Employee Statistics
* Active Employees
* Inactive Employees

#### Employee Dashboard

* Personal Profile
* Employee Information
* Department Details

### Password Management

* Change Password
* Forgot Password
* Password Reset Workflow

### Profile Management

* Profile Image Upload
* Update Personal Details
* Update Contact Information

---

## Technology Stack

* Python
* Django
* PostgreSQL
* HTML5
* CSS3
* Bootstrap
* Git & GitHub

---

## Project Structure

company_portal/

├── accounts/

├── employees/

├── departments/

├── media/

├── templates/

├── static/

├── manage.py

└── requirements.txt

---

## Installation

### Clone Repository

git clone https://github.com/your-username/django-hr-management-system.git

cd django-hr-management-system

### Create Virtual Environment

python -m venv .venv

### Activate Environment

Windows

.venv\Scripts\activate

### Install Dependencies

pip install -r requirements.txt

### Database Migration

python manage.py makemigrations

python manage.py migrate

### Create Superuser

python manage.py createsuperuser

### Run Server

python manage.py runserver

---

## Git Workflow

git checkout development

git pull origin development

git checkout -b feature/authentication-rbac

---

## Screenshots

* Registration Page
* Login Page
* Dashboard
* RBAC Implementation
* Admin Panel

---

## Author

Subhash

Software Engineer | Embedded Systems & Django Developer

---

## License

This project is developed for educational and professional learning purposes.
