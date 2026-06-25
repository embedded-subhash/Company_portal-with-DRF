# Django Company Portal with Django REST Framework (DRF)

A full-stack Company Portal built using Django and Django REST Framework (DRF). The project includes role-based access control, employee and department management, JWT authentication, filtering, pagination, and interactive API documentation using Swagger.

## Features

### User Management

* Custom User Model (AbstractUser)
* User Registration and Login
* Password Change and Reset
* User Profile Management
* Role-Based Access Control (RBAC)

### User Roles

* Admin
* HR
* Manager
* Employee

### Employee Management

* Create Employee
* View Employee Details
* Update Employee Information
* Delete Employee
* Search Employees
* Filter Employees
* Sort Employees
* Pagination Support

### Department Management

* Create Department
* Update Department
* Delete Department
* View Department Details

### REST API Features

* Django REST Framework (DRF)
* Function-Based APIs
* APIView Implementation
* Generic Views
* ModelViewSets
* Routers
* JWT Authentication
* Custom Permissions
* Filtering and Searching
* Pagination
* Swagger Documentation
* ReDoc Documentation

---

## Technology Stack

### Backend

* Python
* Django
* Django REST Framework (DRF)
* PostgreSQL

### Authentication

* Simple JWT

### API Documentation

* drf-yasg (Swagger & ReDoc)

### Filtering

* django-filter

### Version Control

* Git
* GitHub

---

## Project Structure

```text
company_portal/
│
├── accounts/
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   └── urls.py
│
├── employees/
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   └── urls.py
│
├── departments/
│   ├── models.py
│   ├── views.py
│   └── urls.py
│
├── api/
│   ├── serializers.py
│   ├── permissions.py
│   ├── pagination.py
│   ├── filters.py
│   ├── views.py
│   └── urls.py
│
├── templates/
├── media/
├── static/
│
├── manage.py
└── requirements.txt
```

---

## Installation

Clone the repository:

```bash
git clone https://github.com/embedded-subhash/django-company-portal.git
```

Move into the project directory:

```bash
cd django-company-portal
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate the virtual environment:

Windows:

```bash
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Apply migrations:

```bash
python manage.py migrate
```

Create a superuser:

```bash
python manage.py createsuperuser
```

Run the development server:

```bash
python manage.py runserver
```

---

## User Roles and Permissions

| Role     | Permissions                 |
| -------- | --------------------------- |
| Admin    | Full Access                 |
| HR       | Create and Update Employees |
| Manager  | View Team Information       |
| Employee | View Own Profile            |

---

## REST API Endpoints

### Authentication

| Method | Endpoint              | Description          |
| ------ | --------------------- | -------------------- |
| POST   | `/api/token/`         | Generate JWT Token   |
| POST   | `/api/token/refresh/` | Refresh Access Token |

### Employee APIs

| Method | Endpoint               | Description      |
| ------ | ---------------------- | ---------------- |
| GET    | `/api/employees/`      | Employee List    |
| POST   | `/api/employees/`      | Create Employee  |
| GET    | `/api/employees/{id}/` | Employee Details |
| PUT    | `/api/employees/{id}/` | Update Employee  |
| DELETE | `/api/employees/{id}/` | Delete Employee  |

### Department APIs

| Method | Endpoint                 | Description        |
| ------ | ------------------------ | ------------------ |
| GET    | `/api/departments/`      | Department List    |
| POST   | `/api/departments/`      | Create Department  |
| GET    | `/api/departments/{id}/` | Department Details |
| PUT    | `/api/departments/{id}/` | Update Department  |
| DELETE | `/api/departments/{id}/` | Delete Department  |

---

## Search, Filter and Ordering

Search:

```text
/api/employees/?search=subhash
```

Filter by Department:

```text
/api/employees/?department=1
```

Filter by Status:

```text
/api/employees/?status=Active
```

Order by Salary:

```text
/api/employees/?ordering=salary
```

Order by Highest Salary:

```text
/api/employees/?ordering=-salary
```

---

## Pagination

Default page size:

```text
10 records per page
```

Example:

```text
/api/employees/?page=2
```

---

## API Documentation

Swagger UI:

```text
http://127.0.0.1:8000/swagger/
```

ReDoc:

```text
http://127.0.0.1:8000/redoc/
```

---

## Security Features

* Custom User Model
* JWT Authentication
* Role-Based Access Control (RBAC)
* Protected APIs
* Password Reset Functionality
* User Profile Management

---

## Future Enhancements

* Attendance Management System
* Leave Management Module
* Payroll System
* Email Notifications
* Docker Deployment
* CI/CD Pipeline
* Unit Testing
* Cloud Deployment (AWS/Azure)

---

## Author

**Subhash**

Software Engineer | Python & Embedded Systems Developer

GitHub: https://github.com/embedded-subhash

---

## License

This project is developed for learning, portfolio building, and professional development purposes.
