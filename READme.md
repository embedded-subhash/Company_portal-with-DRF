# company_portal — HRMS File Management & Reporting Module

Django + Django REST Framework module implementing enterprise file management
for an HRMS: file uploads, document management, Excel/CSV import-export, PDF
generation, QR codes, and business reporting — built on top of the existing
`company_portal` project.

## Quick Start

```bash
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt

python manage.py migrate
python manage.py seed_data        # creates demo users, departments, 20 employees, attendance
python manage.py createsuperuser  # optional, seed_data already creates admin/admin12345
python manage.py runserver
```

Demo accounts created by `seed_data`:
| Username | Password    | Role                          |
|----------|-------------|--------------------------------|
| admin    | admin12345  | Superuser (Admin/HR access)   |
| hr_user  | hr12345     | HR group                      |
| emp001   | emp12345    | Linked to employee EMP001 (self-service only) |

Open `requests.http` in VS Code (REST Client extension) to exercise every
endpoint, or import the same requests into Postman/Insomnia.

## Folder Structure

```
company_portal/
├── config/                    # Project settings, root urls
├── employees/
│   ├── models.py              # Department, Employee (file fields), Attendance
│   ├── validators.py          # Image/document type + size validation
│   ├── permissions.py         # IsAdmin, IsHR, IsAdminOrHR, IsEmployeeReadOnlySelf
│   ├── serializers.py
│   ├── views.py                # Employee/Department/Attendance ViewSets + all file actions
│   └── management/commands/seed_data.py
├── documents/
│   ├── models.py               # EmployeeDocument
│   ├── serializers.py
│   └── views.py                # Upload / Download / Delete / List (Module 2, 11)
├── reports/
│   ├── models.py               # GeneratedReport (persisted report files)
│   ├── excel_export.py        # Module 3 & 4: Excel import/export
│   ├── csv_handler.py         # Module 5: CSV import/export
│   ├── pdf_generator.py       # Module 6/7/9: profile PDF, salary slip, ID card
│   ├── qr_generator.py        # Module 8: QR code generation
│   ├── report_builder.py      # Module 10 & 12: report + dashboard data & builders
│   ├── serializers.py
│   └── views.py                # generate / download / dashboard / dashboard export
media/
├── employees/<id>/{photo,resume,aadhaar,pan}/
├── documents/<id>/<type>/
├── reports/<type>/
└── id_cards/                   # ID_<employee_id>.pdf, persisted on every /id-card/ call
```

## API Reference (prefix `/api/v1/`)

### Employees & core file uploads
- `GET/POST /employees/` · `GET/PUT/PATCH/DELETE /employees/{id}/`
- `POST /employees/import/` — Excel import (multipart `file`)
- `GET /employees/export/?type=employees|departments|salary|attendance` — Excel export
- `POST /employees/import-csv/` — CSV import
- `GET /employees/export-csv/` — CSV export
- `GET /employees/{id}/profile-pdf/` — Employee profile PDF
- `GET /employees/{id}/salary-slip/?month=June&year=2026` — Salary slip PDF
- `GET /employees/{id}/qr-code/` — Verification QR (PNG)
- `GET /employees/{id}/id-card/` — Employee ID card PDF (photo + QR)

### Documents
- `GET/POST /documents/` · `DELETE /documents/{id}/`
- `GET /documents/{id}/download/` — permission-checked file download

### Reports & Dashboard
- `POST /reports/generate/` — body `{"report_type": "SALARY", "format": "PDF"}`
  - `report_type`: `EMPLOYEE | DEPARTMENT | SALARY | ATTENDANCE | DASHBOARD`
  - `format`: `PDF | EXCEL | CSV` (DASHBOARD supports PDF/EXCEL only)
- `GET /reports/` — list previously generated reports
- `GET /reports/{id}/download/` — download a generated report
- `GET /dashboard/` — live JSON summary (employee/department counts, salary stats, attendance)
- `GET /dashboard/export/?file_format=PDF|EXCEL` — dashboard as a file

> Note: the dashboard export query param is `file_format`, not `format` —
> DRF reserves `?format=` for its own content-negotiation, so reusing it
> causes an unrelated 404/406 from the framework rather than reaching the view.

## Roles & Permissions

- **Admin / superuser** — full access everywhere.
- **HR group** — manage employees, documents, imports/exports, reports, dashboard.
- **Employee (no group)** — read/update only their own `Employee` record
  (via `user` FK) and their own documents, through a restricted serializer
  that keeps `salary`, `status`, `department`, `designation` read-only.

## Validation

- Images (`profile_photo`): `.jpg` / `.jpeg` / `.png`, max 5 MB.
- Documents (`resume`, `aadhaar_document`, `pan_document`, `EmployeeDocument.file`): `.pdf` only, max 5 MB.
- Excel/CSV import: validates required columns, skips invalid/duplicate rows,
  and returns `{total_rows, created, failed, errors}` — no partial employee is ever created for a failed row.

## What Was Verified Live

Every module below was exercised against a running server with seeded data
(20 employees, 4 departments, 10 days of attendance each):

- ✅ Excel import — 2 valid rows created, 1 duplicate correctly rejected with a row-level error
- ✅ CSV import — new employee created, UTF-8 handled
- ✅ Excel export — employees / departments / salary / attendance, all valid `.xlsx`
- ✅ CSV export — valid UTF-8 (BOM) CSV
- ✅ Employee profile PDF, salary slip PDF — valid PDF/1.4 output
- ✅ QR code — valid PNG, decodes to employee verification payload
- ✅ Employee ID card — photo + QR combined into a credit-card-sized PDF
- ✅ Document upload / list / download / delete — full lifecycle, incl. file-type rejection (400 on non-PDF)
- ✅ All 4 report types × 3 formats (12 combinations) generated and downloadable by id
- ✅ Dashboard JSON + PDF/Excel export
- ✅ Role enforcement — HR-only actions return 403 for a plain employee; self-service employee view returns only their own restricted record
