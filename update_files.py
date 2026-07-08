import re

# ---- Update settings.py ----
with open('company_portal/settings.py', 'r', encoding='utf-8') as f:
    content = f.read()

if "'rest_framework'" not in content:
    # Find the INSTALLED_APPS closing bracket after 'accounts'
    content = re.sub(
        r"(    'accounts',\r?\n\])",
        "    'accounts',\n    'rest_framework',\n]\n\nREST_FRAMEWORK = {\n    'DEFAULT_AUTHENTICATION_CLASSES': (\n        'rest_framework_simplejwt.authentication.JWTAuthentication',\n    ),\n}\n\nfrom datetime import timedelta\nSIMPLE_JWT = {\n    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),\n    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),\n}",
        content,
        count=1
    )
    with open('company_portal/settings.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print("settings.py updated successfully")
else:
    print("settings.py already has rest_framework")

# ---- Update accounts/views.py - add imports ----
with open('accounts/views.py', 'r', encoding='utf-8') as f:
    content = f.read()

if 'from rest_framework.views import APIView' not in content:
    content = re.sub(
        r'(from \.forms import ProfileUpdateForm\r?\n)',
        r'\1from rest_framework.views import APIView\nfrom rest_framework.response import Response\nfrom rest_framework import status\nfrom rest_framework_simplejwt.tokens import RefreshToken\n',
        content,
        count=1
    )
    with open('accounts/views.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print("accounts/views.py imports updated successfully")
else:
    print("accounts/views.py already has DRF imports")

# ---- Append APILoginView class to accounts/views.py ----
with open('accounts/views.py', 'r', encoding='utf-8') as f:
    content = f.read()

if 'class APILoginView' not in content:
    api_login_view = '''

class APILoginView(APIView):
    """
    REST API login endpoint. Returns JWT access and refresh tokens.
    POST /api/v1/auth/login/
    Body: { "email": "...", "password": "..." }
    """
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response(
                {'error': 'Email and password are required.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = authenticate(request, username=email, password=password)

        if user is None:
            return Response(
                {'error': 'Invalid email or password.'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        if not user.is_active:
            return Response(
                {'error': 'Account is disabled.'},
                status=status.HTTP_403_FORBIDDEN
            )

        refresh = RefreshToken.for_user(user)

        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'user': {
                'id': user.id,
                'email': user.email,
                'role': getattr(user, 'role', None),
            }
        }, status=status.HTTP_200_OK)
'''
    with open('accounts/views.py', 'a', encoding='utf-8') as f:
        f.write(api_login_view)
    print("APILoginView class appended to accounts/views.py")
else:
    print("accounts/views.py already has APILoginView")

print("All done!")
