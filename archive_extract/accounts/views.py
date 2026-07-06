from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView

from api.responses import ErrorResponse, SuccessResponse

from .serializers import ChangePasswordSerializer, LoginSerializer, UserSerializer


class LoginView(APIView):
    """POST /api/v1/auth/login/  -> returns auth token + user info."""

    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return ErrorResponse(message="Validation Failed", errors=serializer.errors)

        user = serializer.validated_data["user"]
        token, _ = Token.objects.get_or_create(user=user)
        data = {"token": token.key, "user": UserSerializer(user).data}
        return SuccessResponse(message="Login Successful", data=data)


class LogoutView(APIView):
    """POST /api/v1/auth/logout/  -> deletes the auth token."""

    permission_classes = [IsAuthenticated]

    def post(self, request):
        Token.objects.filter(user=request.user).delete()
        return SuccessResponse(message="Logout Successful", data={})


class ChangePasswordView(APIView):
    """POST /api/v1/auth/change-password/"""

    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={"request": request})
        if not serializer.is_valid():
            return ErrorResponse(message="Validation Failed", errors=serializer.errors)

        user = request.user
        user.set_password(serializer.validated_data["new_password"])
        user.save()

        # Invalidate old token, issue a fresh one.
        Token.objects.filter(user=user).delete()
        token = Token.objects.create(user=user)

        return SuccessResponse(
            message="Password Changed Successfully", data={"token": token.key}
        )
