"""
Module 10: Reports Module
Module 12: Dashboard Reports

Builds the four core report types (Employee, Department, Salary, Attendance)
plus the dashboard summary, each in PDF, Excel and CSV where applicable.
Every builder returns (bytes_content, content_type, file_extension).
"""
import csv
import io
from collections import Counter

from django.db.models import Avg, Count, Sum
from django.utils import timezone
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill

from employees.models import Attendance, Department, Employee

styles = getSampleStyleSheet()
title_style = ParagraphStyle("TitleStyle", parent=styles["Title"], fontSize=16)
HEADER_FILL = PatternFill(start_color="1F4E78", end_color="1F4E78", fill_type="solid")
HEADER_FONT = Font(color="FFFFFF", bold=True)

XLSX_CONTENT_TYPE = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
PDF_CONTENT_TYPE = "application/pdf"
CSV_CONTENT_TYPE = "text/csv"


# ---------------------------------------------------------------------------
# Data aggregation
# ---------------------------------------------------------------------------
def employee_report_data():
    active = Employee.objects.filter(status="ACTIVE").count()
    inactive = Employee.objects.filter(status="INACTIVE").count()
    return {"active": active, "inactive": inactive, "total": active + inactive}


def department_report_data():
    return list(
        Department.objects.annotate(
            employee_count=Count("employees"), avg_salary=Avg("employees__salary")
        ).values("name", "employee_count", "avg_salary")
    )


def salary_report_data():
    rows = list(
        Employee.objects.select_related("department").values(
            "employee_id", "first_name", "last_name", "department__name", "salary"
        )
    )
    total_payroll = sum(r["salary"] for r in rows) if rows else 0
    by_department = Counter()
    for r in rows:
        by_department[r["department__name"] or "Unassigned"] += float(r["salary"])
    return {"rows": rows, "total_payroll": float(total_payroll), "by_department": dict(by_department)}


def attendance_report_data():
    counts = Attendance.objects.values("status").annotate(total=Count("id"))
    summary = {"PRESENT": 0, "ABSENT": 0, "LEAVE": 0}
    for row in counts:
        summary[row["status"]] = row["total"]
    return summary


def dashboard_data():
    return {
        "employee_count": Employee.objects.count(),
        "department_count": Department.objects.count(),
        "salary_stats": {
            "total_payroll": float(Employee.objects.aggregate(total=Sum("salary"))["total"] or 0),
            "average_salary": float(Employee.objects.aggregate(avg=Avg("salary"))["avg"] or 0),
        },
        "attendance_summary": attendance_report_data(),
    }


# ---------------------------------------------------------------------------
# PDF builders
# ---------------------------------------------------------------------------
def _simple_pdf(title, table_data, col_widths=None):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, topMargin=20 * mm, bottomMargin=20 * mm)
    table = Table(table_data, colWidths=col_widths)
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1F4E78")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("PADDING", (0, 0), (-1, -1), 6),
    ]))
    elements = [Paragraph(title, title_style), Spacer(1, 10), table]
    doc.build(elements)
    buffer.seek(0)
    return buffer.getvalue()


def employee_report_pdf():
    data = employee_report_data()
    table = [["Metric", "Count"], ["Active Employees", data["active"]],
             ["Inactive Employees", data["inactive"]], ["Total", data["total"]]]
    return _simple_pdf("Employee Report", table, [300, 150])


def department_report_pdf():
    rows = department_report_data()
    table = [["Department", "Code", "Employee Count", "Average Salary"]]
    for r in rows:
        table.append([r["name"], "-", r["employee_count"], f"{(r['avg_salary'] or 0):,.2f}"])
    return _simple_pdf("Department Report", table, [150, 80, 110, 110])


def salary_report_pdf():
    data = salary_report_data()
    table = [["Employee ID", "Name", "Department", "Salary"]]
    for r in data["rows"]:
        table.append([r["employee_id"], f"{r['first_name']} {r['last_name']}", r["department__name"] or "-", f"{r['salary']:,.2f}"])
    table.append(["", "", "Total Payroll", f"{data['total_payroll']:,.2f}"])
    return _simple_pdf("Salary Report — Monthly Payroll", table, [90, 140, 130, 90])


def attendance_report_pdf():
    summary = attendance_report_data()
    table = [["Status", "Count"], ["Present", summary["PRESENT"]],
             ["Absent", summary["ABSENT"]], ["Leave", summary["LEAVE"]]]
    return _simple_pdf("Attendance Report", table, [300, 150])


def dashboard_pdf():
    data = dashboard_data()
    table = [
        ["Metric", "Value"],
        ["Employee Count", data["employee_count"]],
        ["Department Count", data["department_count"]],
        ["Average Salary", f"{data['salary_stats']['average_salary']:,.2f}"],
        ["Present", data["attendance_summary"]["PRESENT"]],
        ["Absent", data["attendance_summary"]["ABSENT"]],
        ["Leave", data["attendance_summary"]["LEAVE"]],
    ]
    return _simple_pdf(f"Dashboard Summary — {timezone.now():%d %b %Y}", table, [300, 150])


# ---------------------------------------------------------------------------
# Excel builders
# ---------------------------------------------------------------------------
def _style_ws_header(ws, headers):
    for idx, header in enumerate(headers, start=1):
        c = ws.cell(row=1, column=idx, value=header)
        c.font = HEADER_FONT
        c.fill = HEADER_FILL


def _wb_bytes(wb):
    buffer = io.BytesIO()
    wb.save(buffer)
    buffer.seek(0)
    return buffer.getvalue()


def employee_report_excel():
    data = employee_report_data()
    wb = Workbook()
    ws = wb.active
    ws.title = "Employee Report"
    _style_ws_header(ws, ["Metric", "Count"])
    ws.append(["Active Employees", data["active"]])
    ws.append(["Inactive Employees", data["inactive"]])
    ws.append(["Total", data["total"]])
    return _wb_bytes(wb)


def department_report_excel():
    wb = Workbook()
    ws = wb.active
    ws.title = "Department Report"
    _style_ws_header(ws, ["Department", "Code", "Employee Count", "Average Salary"])
    for r in department_report_data():
        ws.append([r["name"], "-", r["employee_count"], round(r["avg_salary"] or 0, 2)])
    return _wb_bytes(wb)


def salary_report_excel():
    data = salary_report_data()
    wb = Workbook()
    ws = wb.active
    ws.title = "Salary Report"
    _style_ws_header(ws, ["Employee ID", "Name", "Department", "Salary"])
    for r in data["rows"]:
        ws.append([r["employee_id"], f"{r['first_name']} {r['last_name']}", r["department__name"] or "-", float(r["salary"])])
    ws2 = wb.create_sheet("Department Summary")
    _style_ws_header(ws2, ["Department", "Total Salary"])
    for dept, total in data["by_department"].items():
        ws2.append([dept, total])
    return _wb_bytes(wb)


def attendance_report_excel():
    summary = attendance_report_data()
    wb = Workbook()
    ws = wb.active
    ws.title = "Attendance Report"
    _style_ws_header(ws, ["Status", "Count"])
    ws.append(["Present", summary["PRESENT"]])
    ws.append(["Absent", summary["ABSENT"]])
    ws.append(["Leave", summary["LEAVE"]])
    return _wb_bytes(wb)


def dashboard_excel():
    data = dashboard_data()
    wb = Workbook()
    ws = wb.active
    ws.title = "Dashboard"
    _style_ws_header(ws, ["Metric", "Value"])
    ws.append(["Employee Count", data["employee_count"]])
    ws.append(["Department Count", data["department_count"]])
    ws.append(["Average Salary", round(data["salary_stats"]["average_salary"], 2)])
    ws.append(["Present", data["attendance_summary"]["PRESENT"]])
    ws.append(["Absent", data["attendance_summary"]["ABSENT"]])
    ws.append(["Leave", data["attendance_summary"]["LEAVE"]])
    return _wb_bytes(wb)


# ---------------------------------------------------------------------------
# CSV builders
# ---------------------------------------------------------------------------
def _csv_bytes(headers, rows):
    buffer = io.StringIO()
    writer = csv.writer(buffer)
    writer.writerow(headers)
    writer.writerows(rows)
    return buffer.getvalue().encode("utf-8-sig")


def employee_report_csv():
    data = employee_report_data()
    return _csv_bytes(["Metric", "Count"], [["Active", data["active"]], ["Inactive", data["inactive"]], ["Total", data["total"]]])


def department_report_csv():
    rows = [[r["name"], "-", r["employee_count"], round(r["avg_salary"] or 0, 2)] for r in department_report_data()]
    return _csv_bytes(["Department", "Code", "Employee Count", "Average Salary"], rows)


def salary_report_csv():
    data = salary_report_data()
    rows = [[r["employee_id"], f"{r['first_name']} {r['last_name']}", r["department__name"] or "-", float(r["salary"])] for r in data["rows"]]
    return _csv_bytes(["Employee ID", "Name", "Department", "Salary"], rows)


def attendance_report_csv():
    summary = attendance_report_data()
    return _csv_bytes(["Status", "Count"], [["Present", summary["PRESENT"]], ["Absent", summary["ABSENT"]], ["Leave", summary["LEAVE"]]])


# ---------------------------------------------------------------------------
# Dispatch table used by the view layer
# ---------------------------------------------------------------------------
REPORT_BUILDERS = {
    ("EMPLOYEE", "PDF"): (employee_report_pdf, PDF_CONTENT_TYPE, "pdf"),
    ("EMPLOYEE", "EXCEL"): (employee_report_excel, XLSX_CONTENT_TYPE, "xlsx"),
    ("EMPLOYEE", "CSV"): (employee_report_csv, CSV_CONTENT_TYPE, "csv"),
    ("DEPARTMENT", "PDF"): (department_report_pdf, PDF_CONTENT_TYPE, "pdf"),
    ("DEPARTMENT", "EXCEL"): (department_report_excel, XLSX_CONTENT_TYPE, "xlsx"),
    ("DEPARTMENT", "CSV"): (department_report_csv, CSV_CONTENT_TYPE, "csv"),
    ("SALARY", "PDF"): (salary_report_pdf, PDF_CONTENT_TYPE, "pdf"),
    ("SALARY", "EXCEL"): (salary_report_excel, XLSX_CONTENT_TYPE, "xlsx"),
    ("SALARY", "CSV"): (salary_report_csv, CSV_CONTENT_TYPE, "csv"),
    ("ATTENDANCE", "PDF"): (attendance_report_pdf, PDF_CONTENT_TYPE, "pdf"),
    ("ATTENDANCE", "EXCEL"): (attendance_report_excel, XLSX_CONTENT_TYPE, "xlsx"),
    ("ATTENDANCE", "CSV"): (attendance_report_csv, CSV_CONTENT_TYPE, "csv"),
    ("DASHBOARD", "PDF"): (dashboard_pdf, PDF_CONTENT_TYPE, "pdf"),
    ("DASHBOARD", "EXCEL"): (dashboard_excel, XLSX_CONTENT_TYPE, "xlsx"),
}
