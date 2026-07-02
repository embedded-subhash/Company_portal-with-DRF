import logging
import time

from django.http import HttpResponseForbidden


request_logger = logging.getLogger("request")
app_logger = logging.getLogger("application")
security_logger = logging.getLogger("security")


class RequestLoggingMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        user = (
            request.user
            if request.user.is_authenticated
            else "Anonymous"
        )

        ip = request.META.get(
            "REMOTE_ADDR"
        )

        request_logger.info(
            f"Method: {request.method} | "
            f"URL: {request.path} | "
            f"IP: {ip} | "
            f"User: {user}"
        )

        response = self.get_response(
            request
        )

        return response


class ResponseTimeMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        start_time = time.time()

        response = self.get_response(
            request
        )

        end_time = time.time()

        total_time = (
            end_time - start_time
        ) * 1000

        if total_time > 500:

            app_logger.warning(
                f"Slow Request: "
                f"{request.path} "
                f"took {total_time:.2f} ms"
            )

        return response


class IPRestrictionMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        # Lazy import to avoid AppRegistryNotReady error
        from employees.models import BlockedIP

        ip = request.META.get(
            "REMOTE_ADDR"
        )

        blocked = BlockedIP.objects.filter(
            ip_address=ip
        ).exists()

        if blocked:

            security_logger.warning(
                f"Blocked IP Access Attempt: {ip}"
            )

            return HttpResponseForbidden(
                "403 Forbidden: Your IP address has been blocked."
            )

        response = self.get_response(
            request
        )

        return response