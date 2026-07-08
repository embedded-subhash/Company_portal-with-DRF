from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password as django_validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import PasswordResetToken
from .validators import validate_strong_password

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name", "role", "phone", "is_active"]
        read_only_fields = ["id", "role"]


class RoleAwareTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Adds role/user_id claims to the access token payload so clients
    (React admin, Flutter app) can branch UI without a follow-up
    /profile/ call, without weakening the stateless nature of JWTs.
    """

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["role"] = user.role
        token["username"] = user.username
        return token


class ChangePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)

    def validate_current_password(self, value):
        user = self.context["request"].user
        if not user.check_password(value):
            raise serializers.ValidationError("Current password is incorrect.")
        return value

    def validate_new_password(self, value):
        return validate_strong_password(value)

    def validate(self, attrs):
        if attrs["current_password"] == attrs["new_password"]:
            raise serializers.ValidationError(
                {"new_password": "New password must be different from the current password."}
            )
        return attrs

    def save(self, **kwargs):
        user = self.context["request"].user
        user.set_password(self.validated_data["new_password"])
        user.save(update_fields=["password"])
        return user


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        # Intentionally does NOT raise if the email is unknown -- the view
        # returns a generic success response either way to avoid leaking
        # which emails are registered (Module 11: prevent information leakage).
        return value


class ResetPasswordSerializer(serializers.Serializer):
    token = serializers.CharField()
    new_password = serializers.CharField(write_only=True)

    def validate_new_password(self, value):
        return validate_strong_password(value)

    def validate_token(self, value):
        try:
            reset_token = PasswordResetToken.objects.select_related("user").get(token=value)
        except PasswordResetToken.DoesNotExist:
            raise serializers.ValidationError("Invalid or expired reset token.")
        if not reset_token.is_valid():
            raise serializers.ValidationError("Invalid or expired reset token.")
        self._reset_token = reset_token
        return value

    def save(self, **kwargs):
        reset_token = self._reset_token
        user = reset_token.user
        user.set_password(self.validated_data["new_password"])
        user.save(update_fields=["password"])
        reset_token.mark_used()
        return user
