"""
Standard, reusable API response wrappers.

Every endpoint in this project must return responses shaped like this
instead of raw serializer data:

    Success:
        {"success": true, "message": "...", "data": {...}}

    Validation error:
        {"success": false, "message": "Validation Failed", "errors": {...}}

    Server error:
        {"success": false, "message": "Internal Server Error"}
"""

from rest_framework.response import Response
from rest_framework import status as http_status


class SuccessResponse(Response):
    """200/201-style success envelope."""

    def __init__(self, message="Success", data=None, status=http_status.HTTP_200_OK, **kwargs):
        payload = {
            "success": True,
            "message": message,
            "data": data if data is not None else {},
        }
        super().__init__(data=payload, status=status, **kwargs)


class ErrorResponse(Response):
    """400-style validation/business error envelope."""

    def __init__(
        self,
        message="Validation Failed",
        errors=None,
        status=http_status.HTTP_400_BAD_REQUEST,
        **kwargs,
    ):
        payload = {
            "success": False,
            "message": message,
            "errors": errors if errors is not None else {},
        }
        super().__init__(data=payload, status=status, **kwargs)


class ServerErrorResponse(Response):
    """500-style unexpected error envelope. Never leaks internals to the client."""

    def __init__(self, message="Internal Server Error", status=http_status.HTTP_500_INTERNAL_SERVER_ERROR, **kwargs):
        payload = {"success": False, "message": message}
        super().__init__(data=payload, status=status, **kwargs)
