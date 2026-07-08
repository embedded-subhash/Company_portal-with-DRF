# Company Portal - Secure HRMS REST API

A Django REST Framework based Enterprise HRMS backend implementing secure JWT Authentication, Role-Based Access Control, Password Management, API Security, and Enterprise REST API architecture.

---

## Tech Stack

- Python 3.x
- Django 6
- Django REST Framework
- PostgreSQL
- Simple JWT
- Postman
- Git

---

# Project Structure

```
company_portal/
│
├── accounts/
├── api/
├── employees/
├── departments/
├── logs/
├── media/
├── company_portal/
├── manage.py
└── requirements.txt
```

---

# Features

## Authentication

- JWT Login
- JWT Access Token
- JWT Refresh Token
- Secure Authentication
- Custom User Model
- Email Login

---

## Employee Management

- Employee CRUD
- Department Management
- Profile Image Upload

---

## Security

- JWT Authentication
- Password Hashing
- Authentication Required APIs
- Role-based User Model

---

# Authentication Flow

```
User Login
    │
    ▼
Validate Credentials
    │
    ▼
Generate Access Token
Generate Refresh Token
    │
    ▼
Access Protected APIs
    │
Access Token Expired
    │
    ▼
Refresh Token
    │
    ▼
Generate New Access Token
```

---

# API Endpoints

## Login

POST

```
/api/v1/auth/login/
```

Body

```json
{
    "email":"hr@gmail.com",
    "password":"Hr@12345"
}
```

Response

```json
{
    "access":"<JWT_ACCESS_TOKEN>",
    "refresh":"<JWT_REFRESH_TOKEN>",
    "user":{
        "id":1,
        "email":"hr@gmail.com",
        "role":"HR"
    }
}
```

---

## Refresh Token

POST

```
/api/v1/auth/refresh/
```

Body

```json
{
    "refresh":"<JWT_REFRESH_TOKEN>"
}
```

Response

```json
{
    "access":"<NEW_ACCESS_TOKEN>"
}
```

---

# Authentication

Protected APIs require

```
Authorization: Bearer <ACCESS_TOKEN>
```

Example

```
Authorization: Bearer eyJhbGciOi...
```

---

# User Roles

- ADMIN
- HR
- MANAGER
- EMPLOYEE

---

# Installation

Clone Repository

```bash
git clone <repository-url>
```

Create Virtual Environment

```bash
python -m venv .venv
```

Activate

Windows

```bash
.venv\Scripts\activate
```

Install Requirements

```bash
pip install -r requirements.txt
```

---

# Database

Create PostgreSQL Database

```
company_db
```

Run Migrations

```bash
python manage.py makemigrations

python manage.py migrate
```

Create Superuser

```bash
python manage.py createsuperuser
```

Run Server

```bash
python manage.py runserver
```

---

# Testing

Login API

```
POST

http://127.0.0.1:8000/api/v1/auth/login/
```

Refresh API

```
POST

http://127.0.0.1:8000/api/v1/auth/refresh/
```

---

# JWT Configuration

Access Token Lifetime

```
60 Minutes
```

Refresh Token Lifetime

```
7 Days
```

---

# Completed Modules

- Custom User Model
- Email Authentication
- JWT Login API
- JWT Access Token
- JWT Refresh Token
- Refresh API
- Employee CRUD
- Department CRUD
- PostgreSQL Integration

---

# Upcoming Features

- Logout API
- Token Blacklisting
- Change Password API
- Forgot Password API
- Reset Password API
- Custom Permissions
- Object Level Permissions
- API Rate Limiting
- Secure File Upload
- Security Logging
- HTTPS Configuration
- Audit Logs

---

# Git Workflow

```bash
git checkout development

git pull origin development

git checkout -b feature/jwt-api-security
```

Commit

```bash
git add .

git commit -m "feat: implement JWT authentication"
```

---

# Author

**Subhash**

Software Engineer L1

Blackroth