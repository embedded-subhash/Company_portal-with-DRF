# HRMS REST API Platform (Company Portal)

A complete Django REST Framework project built module-by-module, covering:
enterprise API architecture, advanced serializers, custom role-based
permissions, filtering/searching/ordering, custom pagination, bulk
operations, standardized responses, API versioning, and field validation.

## 1. Project structure

```
company_portal/            Django settings project
├── manage.py
├── requirements.txt
├── company_portal/         settings.py, urls.py, wsgi.py, asgi.py
│
├── api/                    Shared, reusable API infrastructure
│   ├── v1/
│   │   ├── serializers.py  Basic employee shape (Module 2)
│   │   ├── views.py        Employee/Department CRUD, bulk ops, dashboard
│   │   └── urls.py
│   ├── v2/
│   │   ├── serializers.py  Rich employee shape: dept/manager/skills/profile
│   │   ├── views.py
│   │   └── urls.py
│   ├── permissions/         (Module 3)
│   │   ├── admin_permission.py
│   │   ├── hr_permission.py
│   │   └── employee_permission.py
│   ├── pagination.py        (Module 7)
│   ├── filters.py           (Module 4/5/6)
│   ├── responses.py         (Module 9) SuccessResponse / ErrorResponse
│   ├── exceptions.py         Custom DRF exception handler
│   └── validators.py        (Module 11)
│
├── accounts/                Auth: login / logout / change-password, roles
├── employees/                Employee + Skill models
├── departments/              Department model
└── reports/                  AuditLog model + dashboard-support data
```

This mirrors the "Professional Folder Structure" from Module 12, with the
`api/` package holding all cross-cutting concerns and each Django app
owning only its models/admin.

## 2. Setup (VS Code)

```bash
cd company_portal
python -m venv venv
source venv/bin/activate        # venv\Scripts\activate on Windows
pip install -r requirements.txt

python manage.py migrate
python manage.py seed_demo_data  # creates demo users + sample data
python manage.py runserver
```

Open the folder in VS Code — `.vscode/` already contains a debug
configuration (`Django: runserver`), recommended extensions (Python,
Django, REST Client), and a `requests.http` file you can run requests from
directly inside the editor.

### Demo accounts (created by `seed_demo_data`)

| Username     | Password       | Role     |
|--------------|----------------|----------|
| `admin`      | `Admin@12345`  | admin (superuser) |
| `hr_user`    | `Hr@123456`    | hr       |
| `ajay.kumar` | `Employee@123` | employee |

## 3. Auth

```
POST /api/v1/auth/login/            {"username": "...", "password": "..."}
POST /api/v1/auth/logout/
POST /api/v1/auth/change-password/  {"old_password", "new_password", "confirm_password"}
```

Login returns a DRF auth token. Send it on every subsequent request:

```
Authorization: Token <token>
```

## 4. Standard response envelope (Module 9)

Every endpoint returns one of these three shapes — never raw serializer
data:

```jsonc
// Success
{ "success": true,  "message": "Employee Created Successfully", "data": {} }

// Validation error
{ "success": false, "message": "Validation Failed", "errors": {} }

// Server error
{ "success": false, "message": "Internal Server Error" }
```

This is implemented once in `api/responses.py` (`SuccessResponse`,
`ErrorResponse`, `ServerErrorResponse`) and enforced globally via the
custom `EXCEPTION_HANDLER` in `api/exceptions.py`, so unhandled exceptions
never leak a stack trace to the client.

## 5. Employee API (v1)

```
GET    /api/v1/employees/
POST   /api/v1/employees/
GET    /api/v1/employees/{id}/
PUT    /api/v1/employees/{id}/
PATCH  /api/v1/employees/{id}/
DELETE /api/v1/employees/{id}/
GET    /api/v1/employees/profile/me/     view/update own profile
PATCH  /api/v1/employees/profile/me/
```

Sample v1 response shape:

```json
{
  "employee_id": "EMP00001",
  "full_name": "Ajay Kumar",
  "department": { "id": 1, "name": "Engineering" },
  "experience_years": 4,
  "annual_salary": 960000,
  "is_active": true
}
```

`full_name`, `experience_years`, and `annual_salary` are computed via
`SerializerMethodField`s backed by model properties — never stored
directly.

### Filtering (Module 4)

```
GET /api/v1/employees/?department=Engineering
GET /api/v1/employees/?status=active
GET /api/v1/employees/?salary__gte=50000&salary__lte=100000
GET /api/v1/employees/?joining_date_after=2023-01-01&joining_date_before=2023-12-31
GET /api/v1/employees/?designation=Engineer
```

### Searching (Module 5)

```
GET /api/v1/employees/?search=Ajay
```

Searches across `employee_id`, `first_name`, `last_name`, `email`, `phone`.

### Ordering (Module 6)

```
GET /api/v1/employees/?ordering=-salary
GET /api/v1/employees/?ordering=joining_date,first_name
```

Allowed fields: `salary`, `joining_date`, `first_name`, `created_at`.

### Pagination (Module 7)

```json
{
  "count": 2500,
  "next": "http://.../employees/?page=4",
  "previous": "http://.../employees/?page=2",
  "page": 3,
  "page_size": 20,
  "results": []
}
```

Page sizes are set per-resource in `api/pagination.py`:
Employees = 20, Departments = 10, Audit Logs = 50.

### Bulk operations (Module 8)

```
POST  /api/v1/employees/bulk-create/   body: [ {...}, {...} ]
PATCH /api/v1/employees/bulk-update/   body: [ {"id": 1, "salary": 60000}, ... ]
POST  /api/v1/employees/bulk-delete/   body: { "ids": [1, 2, 3] }
```

All three are wrapped in `transaction.atomic()` — if any row in a
bulk-update batch fails validation, the whole batch is rolled back and a
per-index error map is returned.

## 6. Departments API

Full CRUD, admin-only for write operations, 10 records per page.

```
GET/POST      /api/v1/departments/
GET/PUT/PATCH/DELETE  /api/v1/departments/{id}/
```

## 7. Dashboard API

```
GET /api/v1/dashboard/stats/
```

```json
{
  "total_employees": 120,
  "active_employees": 110,
  "inactive_employees": 10,
  "department_count": 6,
  "new_joiners_last_30_days": 4,
  "average_salary": "62500.00"
}
```

## 8. Custom permissions (Module 3)

| Role      | Create | Update | Delete | View |
|-----------|:------:|:------:|:------:|:----:|
| Admin     | ✅ | ✅ | ✅ | ✅ all |
| HR        | ✅ | ✅ | ❌ | ✅ all |
| Employee  | ❌ | ❌ | ❌ | ✅ own profile only |

Implemented as three standalone classes (`IsAdmin`, `IsHR`,
`IsEmployeeReadOnlySelf`) in `api/permissions/`, combined into a single
`EmployeeAccessPolicy` used on `EmployeeViewSet`. Role is stored on
`accounts.UserProfile` (auto-created for every new `User` via a signal).

## 9. Validation (Module 11)

Enforced both as field-level serializer validators (`api/validators.py`)
and as model-level constraints:

* **Employee ID** — must match `EMP00001` (EMP + 5 digits), unique.
* **Email** — must be unique.
* **Phone** — exactly 10 digits.
* **Salary** — cannot be negative.
* **Joining date** — cannot be a future date.

## 10. API versioning (Module 10)

* `/api/v1/employees/` — basic employee data (id, name, department, salary, status).
* `/api/v2/employees/` — adds nested **department**, **manager**, **skills**,
  and a flattened **profile** block (email/phone/tenure), read-only.

## 11. Audit logs

Every create/update/delete/bulk action writes an `AuditLog` row
(`reports` app). List them (admin only, 50/page):

```
GET /api/v1/audit-logs/
```

## 12. Admin site

Django admin is enabled at `/admin/` for quick data inspection —
log in with the `admin` demo account.

## 13. Running tests / quick smoke test

A ready-to-use `requests.http` file is included at the project root for
the VS Code **REST Client** extension — open it, click "Send Request"
above each block (after pasting your login token into the `@token`
variable) to exercise every endpoint described above.
