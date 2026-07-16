from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
urlpatterns = [
    path("", RedirectView.as_view(url="/accounts/login/", permanent=False), name="home"),
    path("admin/", admin.site.urls),
    path("accounts/", include("accounts.urls")),
    path("employees/", include("employees.urls")),
    path("departments/", include("departments.urls")),
    path("api/", include("api.urls")),
    path("api/v1/documents/", include("documents.urls")),
    path("reports/", include("reports.urls")),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)