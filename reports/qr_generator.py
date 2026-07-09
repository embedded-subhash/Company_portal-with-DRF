"""
Module 8: QR Code Generation
Generates verification QR codes for employees (used on ID cards, in salary
slip PDFs, and on the profile page).
"""
import io
import json

import qrcode
from django.conf import settings


def build_verification_payload(employee):
    return {
        "employee_id": employee.employee_id,
        "name": employee.full_name,
        "department": employee.department.name if employee.department else "",
        "verification_url": f"{settings.QR_VERIFICATION_BASE_URL}{employee.employee_id}/",
    }


def generate_employee_qr_png_bytes(employee) -> bytes:
    """Returns raw PNG bytes for the employee's verification QR code."""
    payload = build_verification_payload(employee)
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=8,
        border=2,
    )
    qr.add_data(json.dumps(payload))
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")

    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    return buffer.getvalue()
