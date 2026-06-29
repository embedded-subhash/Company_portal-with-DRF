from rest_framework.response import Response


class SuccessResponse(Response):
    def __init__(self, message="Success", data=None, status=200, **kwargs):
        response_data = {
            "success": True,
            "message": message,
            "data": data if data is not None else {},
        }
        super().__init__(response_data, status=status, **kwargs)


class ErrorResponse(Response):
    def __init__(self, message="Error", errors=None, status=400, **kwargs):
        response_data = {
            "success": False,
            "message": message,
            "errors": errors if errors is not None else {},
        }
        super().__init__(response_data, status=status, **kwargs)
