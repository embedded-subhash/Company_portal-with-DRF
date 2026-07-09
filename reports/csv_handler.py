"""
Module 5: CSV Import & Export
Handles CSV upload (import) and download (export) for employee data,
with UTF-8 encoding, header validation, and duplicate detection.
"""
import csv
import io
from datetime import datetime

from employees.models import Department, Employee

REQUIRED_HEADERS = [
    "Employee ID", "First Name", "Last Name", "Email", "Phone",
    "Department", "Designation", "Salary", "Joining Date",
]


def parse_employee_csv(file_obj):
    """
    Parses an uploaded CSV file (UTF-8), validates headers, detects duplicate
    employee IDs / emails within the file itself and against the DB, and
    returns a summary dict identical in shape to the Excel importer.
    """
    try:
        decoded = file_obj.read().decode("utf-8-sig")
    except UnicodeDecodeError:
        return {"total_rows": 0, "created": 0, "failed": 0, "errors": ["File must be UTF-8 encoded."]}

    reader = csv.DictReader(io.StringIO(decoded))
    headers = reader.fieldnames or []
    missing = [h for h in REQUIRED_HEADERS if h not in headers]
    if missing:
        return {
            "total_rows": 0, "created": 0, "failed": 0,
            "errors": [f"Missing required column(s): {', '.join(missing)}"],
        }

    total_rows = 0
    created = 0
    errors = []
    seen_ids_in_file = set()
    seen_emails_in_file = set()

    for row_num, row in enumerate(reader, start=2):  # row 1 = header
        total_rows += 1
        emp_id = (row.get("Employee ID") or "").strip()
        email = (row.get("Email") or "").strip().lower()

        if not emp_id or not email:
            errors.append(f"Row {row_num}: Employee ID and Email are required.")
            continue
        if emp_id in seen_ids_in_file or email in seen_emails_in_file:
            errors.append(f"Row {row_num}: Duplicate Employee ID/Email within file ({emp_id}).")
            continue
        if Employee.objects.filter(employee_id=emp_id).exists():
            errors.append(f"Row {row_num}: Employee ID '{emp_id}' already exists.")
            continue
        if Employee.objects.filter(email=email).exists():
            errors.append(f"Row {row_num}: Email '{email}' already exists.")
            continue

        try:
            salary = float(row.get("Salary") or 0)
            joining_date = datetime.strptime((row.get("Joining Date") or "").strip(), "%Y-%m-%d").date()
            dept_name = (row.get("Department") or "").strip()
            department, _ = Department.objects.get_or_create(
                name=dept_name, defaults={"code": dept_name[:20].upper() or "GEN"}
            )
            Employee.objects.create(
                employee_id=emp_id,
                first_name=(row.get("First Name") or "").strip(),
                last_name=(row.get("Last Name") or "").strip(),
                email=email,
                phone=(row.get("Phone") or "").strip(),
                department=department,
                designation=(row.get("Designation") or "").strip(),
                salary=salary,
                joining_date=joining_date,
            )
            seen_ids_in_file.add(emp_id)
            seen_emails_in_file.add(email)
            created += 1
        except Exception as exc:  # noqa: BLE001 - surface row-level errors to the caller
            errors.append(f"Row {row_num}: {exc}")

    return {
        "total_rows": total_rows,
        "created": created,
        "failed": total_rows - created,
        "errors": errors,
    }


def build_employee_csv(queryset):
    """Builds an in-memory UTF-8 CSV of employees for export/download."""
    buffer = io.StringIO()
    writer = csv.writer(buffer)
    writer.writerow(REQUIRED_HEADERS + ["Status"])
    for emp in queryset:
        writer.writerow([
            emp.employee_id, emp.first_name, emp.last_name, emp.email, emp.phone,
            emp.department.name if emp.department else "", emp.designation,
            str(emp.salary), emp.joining_date.isoformat(), emp.status,
        ])
    buffer.seek(0)
    return buffer.getvalue().encode("utf-8-sig")
