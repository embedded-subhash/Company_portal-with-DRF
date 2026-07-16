from rest_framework.routers import DefaultRouter
from employees.views import DepartmentViewSet

router = DefaultRouter()
router.register("", DepartmentViewSet, basename="department")

urlpatterns = router.urls