# Enterprise Authentication & Role-Based Access Control (RBAC) System

## Project Overview

The Enterprise Authentication & RBAC System is a Django-based security module designed to implement enterprise-grade user authentication, authorization, custom user management, role-based access control, password management, and profile management.

The system follows industry-standard security practices used in modern software companies to ensure secure access to application resources based on user roles and permissions.

---

## Objectives

* Implement a custom Django User model
* Configure email-based authentication
* Develop user registration and login systems
* Implement role-based access control (RBAC)
* Manage permissions using Django Groups
* Build role-specific dashboards
* Implement password management workflows
* Support profile image uploads and profile updates
* Follow enterprise Git workflow standards

---

## Technology Stack

| Technology                   | Version  |
| ---------------------------- | -------- |
| Python                       | 3.x      |
| Django                       | 5.x      |
| PostgreSQL                   | 17.x     |
| Pillow                       | Latest   |
| Django Authentication System | Built-in |
| Git                          | Latest   |

---

## Authentication Concepts

### Authentication

Authentication verifies the identity of users attempting to access the application.

Examples:

* User Login
* User Logout
* Password Verification
* Session Management

---

### Authorization

Authorization determines the actions users are allowed to perform after authentication.

Examples:

* HR can manage employees
* Managers can supervise departments
* Employees can view their own profiles
* Admins can access all modules

---

## Authentication Workflow

```text
User Login
    │
    ▼
Authentication System
    │
    ▼
Session Created
    │
    ▼
Access Granted
```

---

## Custom User Model

### Why Custom User Model?

Enterprise applications typically require additional user information beyond Django's default User model.

Additional requirements include:

* Employee ID
* Mobile Number
* Department
* Profile Image
* User Role
* Active Status

---

## User Model Fields

| Field         | Type                |
| ------------- | ------------------- |
| username      | CharField           |
| email         | EmailField (Unique) |
| employee_id   | CharField (Unique)  |
| phone         | CharField           |
| role          | CharField           |
| profile_image | ImageField          |
| is_active     | BooleanField        |
| is_staff      | BooleanField        |
| date_joined   | DateTimeField       |

---

## User Roles

The system supports four enterprise roles:

| Role     | Access Level            |
| -------- | ----------------------- |
| ADMIN    | Full System Access      |
| HR       | Employee Management     |
| MANAGER  | Department Supervision  |
| EMPLOYEE | Personal Profile Access |

---

## Registration Module

### Registration URL

```text
/accounts/register/
```

---

### Registration Fields

* First Name
* Last Name
* Email Address
* Employee ID
* Phone Number
* Password
* Confirm Password
* User Role

---

## Validation Rules

### Email Validation

Requirements:

* Must be unique
* Valid email format

Example:

```text
employee@company.com
```

---

### Employee ID Validation

Requirements:

* Unique identifier
* Company standard format

Examples:

```text
EMP001
EMP002
EMP003
```

---

### Password Policy

Password requirements:

* Minimum 8 characters
* At least one uppercase letter
* At least one lowercase letter
* At least one numeric digit
* At least one special character

Example:

```text
Password@123
```

---

## Login & Logout System

### Login URL

```text
/accounts/login/
```

Features:

* Email-based authentication
* Session creation
* Dashboard redirection
* Error handling

---

### Logout URL

```text
/accounts/logout/
```

Features:

* Session destruction
* Secure logout
* Login page redirection

---

## Role-Based Access Control (RBAC)

The application implements custom decorators for role protection.

### Admin Access

```python
@admin_required
def delete_employee(request):
    pass
```

---

### HR Access

```python
@hr_required
def manage_recruitment(request):
    pass
```

---

### Manager Access

```python
@manager_required
def team_dashboard(request):
    pass
```

---

## Django Groups & Permissions

### System Groups

The following groups are created:

* Admin
* HR
* Manager
* Employee

---

## Employee Permissions

| Permission      | Description               |
| --------------- | ------------------------- |
| add_employee    | Create employees          |
| change_employee | Update employees          |
| delete_employee | Remove employees          |
| view_employee   | View employee information |

---

## Dynamic Permission Assignment

Example:

```python
if user.role == "HR":
    user.user_permissions.add(
        add_employee_permission,
        change_employee_permission,
        delete_employee_permission,
        view_employee_permission
    )
```

---

## Dashboard System

### Admin Dashboard

Features:

* Total Employees
* Total Departments
* User Statistics
* System Overview

---

### HR Dashboard

Features:

* Employee Management
* Recruitment Metrics
* Department Information

---

### Employee Dashboard

Features:

* User Profile
* Salary Information
* Department Details
* Personal Information

---

## Dashboard Redirection Logic

```python
if role == "ADMIN":
    return redirect("admin_dashboard")

elif role == "HR":
    return redirect("hr_dashboard")

elif role == "EMPLOYEE":
    return redirect("employee_dashboard")
```

---

## Password Management

### Change Password

URL:

```text
/accounts/change-password/
```

Features:

* Old password verification
* New password validation
* Secure password update

---

### Forgot Password

URL:

```text
/accounts/forgot-password/
```

Features:

* Email verification
* Token generation
* Reset link delivery

---

### Password Reset Workflow

```text
User Request
    │
    ▼
Generate Email Token
    │
    ▼
Send Reset Link
    │
    ▼
User Creates New Password
    │
    ▼
Password Updated
```

---

## User Profile Management

Users can:

* Upload profile images
* Update phone numbers
* Modify personal information
* Change passwords
* View account details

---

## Project Structure

```text
company_portal/
│
├── accounts/
│   ├── models.py
│   ├── forms.py
│   ├── views.py
│   ├── urls.py
│   ├── decorators.py
│   ├── permissions.py
│   ├── admin.py
│   │
│   ├── templates/
│   │   └── accounts/
│   │       ├── register.html
│   │       ├── login.html
│   │       ├── profile.html
│   │       └── dashboard.html
│
├── employees/
├── departments/
├── media/
└── requirements.txt
```

---

## Enterprise Features Implemented

### Authentication Features

* Custom User Model
* Email-Based Login
* Secure Password Hashing
* User Registration
* Session Management
* Logout Functionality

---

### Authorization Features

* Role-Based Access Control
* Custom Decorators
* Django Groups
* Dynamic Permissions
* Dashboard Restrictions

---

### User Management Features

* Profile Image Upload
* User Profile Management
* Password Reset
* Change Password
* Active/Inactive Users

---

## Git Workflow

Switch to Development Branch:

```bash
git checkout development
```

Pull Latest Changes:

```bash
git pull origin development
```

Create Feature Branch:

```bash
git checkout -b feature/authentication-rbac
```

---

## Commit History

```text
feat: create custom user model

feat: implement login and logout

feat: add role based access control

feat: implement dashboard redirection

feat: add password management
```

---

## Company-Level Assignment

### Employee User Management System

Implemented Features:

* User Registration
* User Login
* User Logout
* Profile Management
* Password Reset
* Role-Based Access Control
* Dashboard Redirection
* Permission Management
* Profile Image Upload

---

## Submission Requirements

The following deliverables are included:

* GitHub Repository URL
* Registration Screenshot
* Login Screenshot
* Dashboard Screenshot
* RBAC Screenshot
* Admin Panel Screenshot
* Pull Request URL
* README Documentation

---

## Jira Story

### Story Title

Build Enterprise Authentication & RBAC System

---

### Description

As a Django Backend Developer Trainee,

I need to implement authentication, authorization, custom user management, and role-based access control so that the application follows enterprise security standards.

---

## Acceptance Criteria

* Custom User Model implemented
* Registration and Login working
* Logout functionality implemented
* RBAC implemented
* Role-based dashboards created
* Permissions assigned correctly
* Password management working
* User profile management implemented
* Git workflow followed

---

## Priority

High

---

## Estimated Effort

8 Hours

---

## Learning Outcomes

After completing this project, developers will understand:

* Django Authentication Framework
* Custom User Models
* Role-Based Access Control
* Django Permissions & Groups
* Session Management
* Password Security
* User Profile Management
* Enterprise Security Standards
* Professional Backend Development Practices

---

## Author

**Subhash**

Software Engineer | Django Backend Developer | Authentication & Security Learner
