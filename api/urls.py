from django.urls import path, include
from rest_framework.routers import DefaultRouter

from rest_framework_simplejwt.views import (
    TokenRefreshView
)

from .views import (
    EmailTokenObtainPairView,
    EmployeeViewSet,
    DepartmentViewSet,
    UserViewSet
)


router = DefaultRouter()

router.register(
    r'employees',
    EmployeeViewSet,
    basename='employee'
)

router.register(
    r'departments',
    DepartmentViewSet,
    basename='department'
)

router.register(
    r'users',
    UserViewSet,
    basename='user'
)


urlpatterns = [

    path(
        '',
        include(router.urls)
    ),

    path(
        'token/',
        EmailTokenObtainPairView.as_view(),
        name='token_obtain_pair'
    ),

    path(
        'token/refresh/',
        TokenRefreshView.as_view(),
        name='token_refresh'
    ),

]
