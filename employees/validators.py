import os

from django.conf import settings
from django.core.exceptions import ValidationError


def _validate_extension(value, allowed_extensions):
    ext = os.path.splitext(value.name)[1].lower()
    if ext not in allowed_extensions:
        raise ValidationError(
            f"Unsupported file type '{ext}'. Allowed types: {', '.join(allowed_extensions)}"
        )


def _validate_size(value, max_mb):
    max_bytes = max_mb * 1024 * 1024
    if value.size > max_bytes:
        raise ValidationError(f"File too large. Maximum allowed size is {max_mb} MB.")


def validate_image_file(value):
    """Validates profile photos etc. -> JPG/PNG, max size from settings."""
    _validate_extension(value, settings.ALLOWED_IMAGE_EXTENSIONS)
    _validate_size(value, settings.MAX_IMAGE_UPLOAD_SIZE_MB)


def validate_document_file(value):
    """Validates resumes / aadhaar / pan / other documents -> PDF, max size from settings."""
    _validate_extension(value, settings.ALLOWED_DOCUMENT_EXTENSIONS)
    _validate_size(value, settings.MAX_DOCUMENT_UPLOAD_SIZE_MB)
