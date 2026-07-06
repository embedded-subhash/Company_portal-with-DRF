from rest_framework.routers import DefaultRouter

from .views import EmployeeViewSetV2

router = DefaultRouter()
router.register(r"employees", EmployeeViewSetV2, basename="employee-v2")

urlpatterns = router.urls
