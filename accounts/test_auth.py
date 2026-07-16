from datetime import timedelta
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken
from django.urls import reverse

from accounts.models import User
from accounts.services import PasswordResetService


class UserManagerTests(TestCase):
    def test_create_user_assigns_defaults_and_unique_employee_id(self):
        user = User.objects.create_user(email="employee@example.com", password="StrongPass123!")
        self.assertEqual(user.role, "EMPLOYEE")
        self.assertTrue(user.check_password("StrongPass123!"))
        self.assertTrue(user.employee_id.startswith("EMP"))

    def test_create_superuser_uses_admin_defaults(self):
        admin = User.objects.create_superuser(email="admin@example.com", password="StrongPass123!")
        self.assertTrue(admin.is_staff)
        self.assertTrue(admin.is_superuser)
        self.assertEqual(admin.role, "ADMIN")

    def test_create_user_rejects_missing_email(self):
        with self.assertRaises(ValueError):
            User.objects.create_user(email="", password="StrongPass123!")


class AuthenticationApiTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="auth@example.com", password="StrongPass123!")

    def test_login_returns_tokens_for_valid_credentials(self):
        response = self.client.post(
            reverse("api-login"),
            {"email": "auth@example.com", "password": "StrongPass123!"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.json())
        self.assertIn("refresh", response.json())
        self.assertEqual(response.json()["user"]["email"], "auth@example.com")

    def test_login_rejects_invalid_credentials(self):
        response = self.client.post(
            reverse("api-login"),
            {"email": "auth@example.com", "password": "wrong-password"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_requires_email_and_password(self):
        response = self.client.post(reverse("api-login"), {"email": ""}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_inactive_user_is_rejected(self):
        self.user.is_active = False
        self.user.save(update_fields=["is_active"])
        response = self.client.post(
            reverse("api-login"),
            {"email": "auth@example.com", "password": "StrongPass123!"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_refresh_token_returns_new_access_token(self):
        login_response = self.client.post(
            reverse("api-login"),
            {"email": "auth@example.com", "password": "StrongPass123!"},
            format="json",
        )
        refresh_token = login_response.json()["refresh"]
        response = self.client.post(reverse("token-refresh"), {"refresh": refresh_token}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.json())

    def test_refresh_token_rejects_invalid_token(self):
        response = self.client.post(reverse("token-refresh"), {"refresh": "not-a-valid-token"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_password_reset_service_sends_email(self):
        with patch("accounts.services.send_mail") as mock_send_mail:
            PasswordResetService.initiate_reset(self.user)
        self.assertEqual(mock_send_mail.call_count, 1)
        self.assertIn(self.user.email, mock_send_mail.call_args.kwargs["recipient_list"])

    def test_password_reset_service_invalidates_existing_tokens(self):
        first_token = PasswordResetService.issue_token(self.user)
        second_token = PasswordResetService.issue_token(self.user)
        self.assertNotEqual(first_token.token, second_token.token)
        self.assertIsNotNone(second_token)
