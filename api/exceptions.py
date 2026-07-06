"""
Custom exception handler so that ALL errors raised anywhere in the API
(views, serializers, permissions) come back in the standard response
envelope defined in api/responses.py, instead of DRF's raw default shape.
"""

import logging

from rest_framework.views import exception_handler as drf_exception_handler
from rest_framework.exceptions import ValidationError

logger = logging.getLogger(__name__)


def custom_exception_handler(exc, context):
    response = drf_exception_handler(exc, context)

    if response is None:
        # Anything DRF didn't recognize (unhandled Python exception) -> 500.
        logger.exception("Unhandled server error", exc_info=exc)
        return _server_error()

    if isinstance(exc, ValidationError):
        response.data = {
            "success": False,
            "message": "Validation Failed",
            "errors": response.data,
        }
        return response

    # Any other handled DRF exception (NotFound, PermissionDenied,
    # AuthenticationFailed, Throttled, MethodNotAllowed, etc).
    detail = response.data.get("detail") if isinstance(response.data, dict) else response.data
    response.data = {
        "success": False,
        "message": str(detail) if detail else "Request Failed",
        "errors": response.data if not isinstance(response.data, dict) or "detail" not in response.data else {},
    }
    return response


def _server_error():
    from api.responses import ServerErrorResponse

    return ServerErrorResponse()
