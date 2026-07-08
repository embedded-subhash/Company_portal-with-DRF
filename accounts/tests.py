from django.test import TestCase
from django.contrib.auth import get_user_model


class UserManagerTests(TestCase):
    def test_create_superuser_with_defaults(self):
        User = get_user_model()

        user = User.objects.create_superuser(
            email='admin@example.com',
            password='StrongPass123!',
        )

        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_active)
        self.assertEqual(user.email, 'admin@example.com')
        self.assertTrue(user.check_password('StrongPass123!'))

    def test_create_superuser_uses_unique_employee_id(self):
        User = get_user_model()

        existing_user = User.objects.create_user(
            email='employee@example.com',
            password='StrongPass123!',
        )
        superuser = User.objects.create_superuser(
            email='admin2@example.com',
            password='StrongPass123!',
        )

        self.assertNotEqual(existing_user.employee_id, superuser.employee_id)
