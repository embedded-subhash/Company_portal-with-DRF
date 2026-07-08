"""
Standardized error-response envelope (Module 11: API Security Best
Practices -- standard error responses, prevent information leakage).

Every DRF exception is normalized to:
    {"error": {"code": "<http-status-slug>", "message": "...", "details": {...}}}
so clients never see raw tracebacks, and unexpected 500s are reduced
to a generic message instead of leaking internals.
"""
from rest_framework.views import exception_handler
from rest_framework import status


def standard_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is None:
        # Unhandled exception -- never leak the raw exception message.
        return None

    detail = response.data
    message = "Request could not be processed."
    if isinstance(detail, dict) and "detail" in detail and len(detail) == 1:
        message = str(detail["detail"])
    elif isinstance(detail, dict):
        message = "Validation failed."
    elif isinstance(detail, list) and detail:
        message = str(detail[0])

    response.data = {
        "error": {
            "code": response.status_code,
            "message": message,
            "details": detail if isinstance(detail, dict) else None,
        }
    }
    return response
