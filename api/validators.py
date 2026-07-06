"""
Standalone reusable validators for employee data (Module 11).

These are used both at the serializer field level and can be reused
directly on model fields.
"""

import re
from datetime import date

from rest_framework import serializers

EMPLOYEE_ID_PATTERN = re.compile(r"^EMP\d{5}$")
PHONE_PATTERN = re.compile(r"^\d{10}$")


def validate_employee_id_format(value):
    """Employee ID must look like EMP00001."""
    if not EMPLOYEE_ID_PATTERN.match(value):
        raise serializers.ValidationError(
            "Employee ID must be in the format EMP00001 (EMP followed by 5 digits)."
        )
    return value


def validate_phone_number(value):
    """Phone must be exactly 10 digits."""
    if not PHONE_PATTERN.match(value):
        raise serializers.ValidationError("Phone number must be exactly 10 digits.")
    return value


def validate_salary_non_negative(value):
    """Salary cannot be negative."""
    if value is None or value < 0:
        raise serializers.ValidationError("Salary cannot be negative.")
    return value


def validate_joining_date_not_future(value):
    """Joining date cannot be in the future."""
    if value and value > date.today():
        raise serializers.ValidationError("Joining date cannot be a future date.")
    return value
