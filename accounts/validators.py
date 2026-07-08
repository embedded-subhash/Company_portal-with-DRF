"""
Reusable field- and file-level validators (Module 8 & 9 of the spec).

Split into:
  - password validation (delegates to Django's configured validators)
  - request field validators (employee id, phone, salary, joining date)
  - secure file upload validation (extension + MIME + size)
"""
import re
from datetime import date

from django.core.exceptions import ValidationError as DjangoValidationError
from django.contrib.auth.password_validation import validate_password as django_validate_password
from rest_framework import serializers

EMPLOYEE_ID_RE = re.compile(r"^EMP\d{5}$")
PHONE_RE = re.compile(r"^\d{10}$")

ALLOWED_IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png"}
ALLOWED_IMAGE_MIME_TYPES = {"image/jpeg", "image/png"}
MAX_UPLOAD_SIZE_BYTES = 2 * 1024 * 1024  # 2 MB


def validate_strong_password(value):
    """Wraps Django's password validators and surfaces DRF-style errors."""
    try:
        django_validate_password(value)
    except DjangoValidationError as exc:
        raise serializers.ValidationError(list(exc.messages))
    return value


def validate_employee_id(value):
    if not EMPLOYEE_ID_RE.match(value):
        raise serializers.ValidationError("Employee ID must match the format EMP00001.")
    return value


def validate_phone_number(value):
    if not PHONE_RE.match(value):
        raise serializers.ValidationError("Phone number must be exactly 10 digits.")
    return value


def validate_salary(value):
    if value is None or value <= 0:
        raise serializers.ValidationError("Salary must be a positive number.")
    return value


def validate_joining_date(value):
    if value > date.today():
        raise serializers.ValidationError("Joining date cannot be in the future.")
    return value


def validate_profile_image(file_obj):
    """
    Defense-in-depth upload validation:
      1. Extension allow-list
      2. Declared MIME type allow-list
      3. Magic-byte sniff of the actual file content (catches renamed .exe/.zip/.js/.bat)
      4. Size ceiling
    """
    import os

    name = getattr(file_obj, "name", "")
    ext = os.path.splitext(name)[1].lower()
    if ext not in ALLOWED_IMAGE_EXTENSIONS:
        raise serializers.ValidationError(
            f"Unsupported file extension '{ext}'. Only JPG and PNG are allowed."
        )

    content_type = getattr(file_obj, "content_type", None)
    if content_type not in ALLOWED_IMAGE_MIME_TYPES:
        raise serializers.ValidationError(
            f"Unsupported content type '{content_type}'. Only image/jpeg and image/png are allowed."
        )

    if file_obj.size > MAX_UPLOAD_SIZE_BYTES:
        raise serializers.ValidationError("File too large. Maximum allowed size is 2 MB.")

    # Sniff the real bytes rather than trusting the client-supplied
    # extension/content-type, which are trivially spoofable.
    file_obj.seek(0)
    header = file_obj.read(12)
    file_obj.seek(0)

    is_png = header.startswith(b"\x89PNG\r\n\x1a\n")
    is_jpeg = header.startswith(b"\xff\xd8\xff")
    if not (is_png or is_jpeg):
        raise serializers.ValidationError(
            "File content does not match a valid JPG or PNG image."
        )

    return file_obj
