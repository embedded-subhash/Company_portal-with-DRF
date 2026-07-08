from django.http import Http404
from rest_framework import status
from rest_framework.exceptions import (
    AuthenticationFailed,
    NotAuthenticated,
    NotFound,
    PermissionDenied,
    ValidationError,
)
from rest_framework.views import exception_handler

from api.responses import ErrorResponse


def _flatten_error_detail(detail):
    if isinstance(detail, dict):
        return {
            key: _flatten_error_detail(value)
            for key, value in detail.items()
        }

    if isinstance(detail, list):
        if not detail:
            return ""
        if len(detail) == 1:
            return _flatten_error_detail(detail[0])
        return [_flatten_error_detail(item) for item in detail]

    return str(detail)


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is None:
        if isinstance(exc, Http404):
            return ErrorResponse(
                message="Not Found",
                errors={"detail": "Requested resource was not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        return ErrorResponse(
            message="Server Error",
            errors={"detail": "An unexpected error occurred."},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    if isinstance(exc, ValidationError):
        message = "Validation Error"
    elif isinstance(exc, (AuthenticationFailed, NotAuthenticated)):
        message = "Authentication Failed"
    elif isinstance(exc, PermissionDenied):
        message = "Permission Denied"
    elif isinstance(exc, NotFound):
        message = "Not Found"
    else:
        message = response.data.get("detail", "API Error") if isinstance(response.data, dict) else "API Error"

    return ErrorResponse(
        message=message,
        errors=_flatten_error_detail(response.data),
        status=response.status_code,
    )
