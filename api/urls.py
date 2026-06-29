from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    EmailTokenObtainPairView,
    EmployeeV1ViewSet,
    EmployeeV2ViewSet,
    DepartmentViewSet,
    LogoutView,
    RefreshTokenView,
    UserViewSet
)
from audit_logs.views import AuditLogViewSet


v1_router = DefaultRouter()

v1_router.register(
    r'employees',
    EmployeeV1ViewSet,
    basename='employee'
)

v1_router.register(
    r'departments',
    DepartmentViewSet,
    basename='department'
)

v1_router.register(
    r'users',
    UserViewSet,
    basename='user'
)

v1_router.register(
    r'audit-logs',
    AuditLogViewSet,
    basename='audit-log'
)

employee_v2_list = EmployeeV2ViewSet.as_view({
    'get': 'list',
    'post': 'create',
})
employee_v2_detail = EmployeeV2ViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy',
})
department_v2_list = DepartmentViewSet.as_view({
    'get': 'list',
    'post': 'create',
})
department_v2_detail = DepartmentViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy',
})

urlpatterns = [

    path(
        'v1/',
        include(v1_router.urls)
    ),

    path(
        'v2/employees/',
        employee_v2_list,
        name='v2-employee-list'
    ),

    path(
        'v2/employees/<int:pk>/',
        employee_v2_detail,
        name='v2-employee-detail'
    ),

    path(
        'v2/departments/',
        department_v2_list,
        name='v2-department-list'
    ),

    path(
        'v2/departments/<int:pk>/',
        department_v2_detail,
        name='v2-department-detail'
    ),

    path(
        'v1/auth/login/',
        EmailTokenObtainPairView.as_view(),
        name='token_obtain_pair'
    ),

    path(
        'v1/auth/refresh/',
        RefreshTokenView.as_view(),
        name='token_refresh'
    ),

    path(
        'v1/auth/logout/',
        LogoutView.as_view(),
        name='token_logout'
    ),

    path(
        '',
        include(v1_router.urls)
    ),

]
