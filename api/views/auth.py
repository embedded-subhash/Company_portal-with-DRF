from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from accounts.models import User
from audit_logs.services import create_audit_log
from api.responses import SuccessResponse
from api.serializers import EmailTokenObtainPairSerializer
from api.throttling import LoginRateThrottle


def _client_ip(request):
    ip_address = request.META.get("HTTP_X_FORWARDED_FOR")
    if ip_address:
        return ip_address.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR")


class EmailTokenObtainPairView(TokenObtainPairView):
    serializer_class = EmailTokenObtainPairSerializer
    throttle_classes = [LoginRateThrottle]

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        email = request.data.get("email") or request.data.get("username")
        user = User.objects.filter(email=email).first()
        create_audit_log(
            user=user,
            action="Login",
            module="Authentication",
            ip_address=_client_ip(request),
        )
        return SuccessResponse(
            "Login Successful",
            response.data,
            status=response.status_code,
        )


class RefreshTokenView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        return SuccessResponse(
            "Token Refreshed Successfully",
            response.data,
            status=response.status_code,
        )


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get("refresh")

        if refresh_token:
            token = RefreshToken(refresh_token)
            if hasattr(token, "blacklist"):
                token.blacklist()

        create_audit_log(
            user=request.user,
            action="Logout",
            module="Authentication",
            ip_address=_client_ip(request),
        )
        return SuccessResponse(
            "Logout Successful",
            {},
            status=status.HTTP_200_OK,
        )
