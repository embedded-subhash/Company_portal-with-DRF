from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import EmployeeDocumentViewSet

router = DefaultRouter()
router.register(
    "",
    EmployeeDocumentViewSet,
    basename="documents",
)

urlpatterns = [
    path("", include(router.urls)),
]