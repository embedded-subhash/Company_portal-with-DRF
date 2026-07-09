"""
Module 6: PDF Generation (Employee Profile)
Module 7: Salary Slip Generation
Module 9: Employee ID Card Generator

All generators return raw PDF bytes so callers (views) decide whether to
stream them as a download or persist them to the reports app.
"""
import io

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image

from .qr_generator import generate_employee_qr_png_bytes

COMPANY_NAME = "Company Portal Pvt. Ltd."
styles = getSampleStyleSheet()
title_style = ParagraphStyle("TitleStyle", parent=styles["Title"], fontSize=18, spaceAfter=12)
heading_style = ParagraphStyle("HeadingStyle", parent=styles["Heading2"], textColor=colors.HexColor("#1F4E78"))


# ---------------------------------------------------------------------------
# Module 6: Employee Profile PDF
# ---------------------------------------------------------------------------
def generate_employee_profile_pdf(employee) -> bytes:
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, topMargin=20 * mm, bottomMargin=20 * mm)
    elements = [
        Paragraph(COMPANY_NAME, title_style),
        Paragraph("Employee Profile", heading_style),
        Spacer(1, 10),
    ]

    data = [
        ["Employee ID", employee.employee_id],
        ["Name", employee.full_name],
        ["Department", employee.department.name if employee.department else "-"],
        ["Designation", employee.designation],
        ["Salary", f"{employee.salary:,.2f}"],
        ["Joining Date", employee.joining_date.strftime("%d-%b-%Y")],
        ["Email", employee.email],
        ["Phone", employee.phone],
        ["Status", employee.get_status_display()],
    ]
    table = Table(data, colWidths=[150, 300])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#EAF1F8")),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("PADDING", (0, 0), (-1, -1), 6),
    ]))
    elements.append(table)

    doc.build(elements)
    buffer.seek(0)
    return buffer.getvalue()


# ---------------------------------------------------------------------------
# Module 7: Salary Slip Generation
# ---------------------------------------------------------------------------
def generate_salary_slip_pdf(employee, month: str, year: int, allowances=None, deductions=None) -> bytes:
    allowances = allowances or {"HRA": float(employee.salary) * 0.20, "Special Allowance": float(employee.salary) * 0.10}
    deductions = deductions or {"Provident Fund": float(employee.salary) * 0.12, "Professional Tax": 200.0}

    basic = float(employee.salary)
    total_allowances = sum(allowances.values())
    total_deductions = sum(deductions.values())
    net_salary = basic + total_allowances - total_deductions

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, topMargin=20 * mm, bottomMargin=20 * mm)
    elements = [
        Paragraph(COMPANY_NAME, title_style),
        Paragraph(f"Salary Slip — {month} {year}", heading_style),
        Spacer(1, 6),
        Paragraph(f"Employee: {employee.full_name} ({employee.employee_id})", styles["Normal"]),
        Paragraph(f"Department: {employee.department.name if employee.department else '-'} | Designation: {employee.designation}", styles["Normal"]),
        Spacer(1, 12),
    ]

    earnings_rows = [["Earnings", "Amount"], ["Basic Salary", f"{basic:,.2f}"]]
    earnings_rows += [[k, f"{v:,.2f}"] for k, v in allowances.items()]
    earnings_rows.append(["Total Earnings", f"{basic + total_allowances:,.2f}"])

    deduction_rows = [["Deductions", "Amount"]]
    deduction_rows += [[k, f"{v:,.2f}"] for k, v in deductions.items()]
    deduction_rows.append(["Total Deductions", f"{total_deductions:,.2f}"])

    combined = Table([
        [Table(earnings_rows, colWidths=[120, 90]), Table(deduction_rows, colWidths=[120, 90])]
    ])
    for t in (earnings_rows, deduction_rows):
        pass
    style = TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1F4E78")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("PADDING", (0, 0), (-1, -1), 5),
    ])
    earnings_table = Table(earnings_rows, colWidths=[150, 100])
    earnings_table.setStyle(style)
    deductions_table = Table(deduction_rows, colWidths=[150, 100])
    deductions_table.setStyle(style)

    elements.append(Table([[earnings_table, deductions_table]], colWidths=[260, 260]))
    elements.append(Spacer(1, 16))

    net_table = Table([["Net Salary", f"Rs. {net_salary:,.2f}"]], colWidths=[150, 100])
    net_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#DFF3E3")),
        ("FONTNAME", (0, 0), (-1, -1), "Helvetica-Bold"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("PADDING", (0, 0), (-1, -1), 6),
    ]))
    elements.append(net_table)

    doc.build(elements)
    buffer.seek(0)
    return buffer.getvalue()


# ---------------------------------------------------------------------------
# Module 9: Employee ID Card Generator
# ---------------------------------------------------------------------------
def generate_employee_id_card_pdf(employee, valid_till) -> bytes:
    buffer = io.BytesIO()
    card_size = (86 * mm, 54 * mm)  # standard credit-card size, wide format
    doc = SimpleDocTemplate(buffer, pagesize=card_size, topMargin=4 * mm, bottomMargin=4 * mm,
                             leftMargin=4 * mm, rightMargin=4 * mm)

    qr_bytes = generate_employee_qr_png_bytes(employee)
    qr_image = Image(io.BytesIO(qr_bytes), width=18 * mm, height=18 * mm)

    photo_cell = "No Photo"
    if employee.profile_photo:
        try:
            photo_cell = Image(employee.profile_photo.path, width=18 * mm, height=18 * mm)
        except Exception:
            photo_cell = "No Photo"

    small_style = ParagraphStyle("Small", parent=styles["Normal"], fontSize=7, leading=9)
    name_style = ParagraphStyle("Name", parent=styles["Normal"], fontSize=9, leading=11, fontName="Helvetica-Bold")

    header = Paragraph(f"<b>{COMPANY_NAME}</b>", ParagraphStyle("Header", fontSize=8, alignment=1))
    info = Paragraph(
        f"{employee.full_name}<br/>{employee.employee_id}<br/>"
        f"{employee.department.name if employee.department else '-'}<br/>"
        f"Valid till: {valid_till.strftime('%b %Y')}",
        small_style,
    )

    body = Table([[photo_cell, info, qr_image]], colWidths=[20 * mm, 40 * mm, 20 * mm])
    body.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "MIDDLE")]))

    elements = [header, Spacer(1, 4), body]
    doc.build(elements)
    buffer.seek(0)
    return buffer.getvalue()
