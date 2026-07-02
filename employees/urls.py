from django.urls import path

from .views import (
    EmployeeListView,
    EmployeeCreateView,
    EmployeeDetailView,
    EmployeeUpdateView,
    EmployeeDeleteView,
    slow_view,
    dashboard
)

urlpatterns = [

    path(
        '',
        EmployeeListView.as_view(),
        name='employee_list'
    ),

    path(
        'dashboard/',
        dashboard,
        name='dashboard'
    ),

    path(
        'create/',
        EmployeeCreateView.as_view(),
        name='employee_create'
    ),

    path(
        '<int:pk>/',
        EmployeeDetailView.as_view(),
        name='employee_detail'
    ),

    path(
        'update/<int:pk>/',
        EmployeeUpdateView.as_view(),
        name='employee_update'
    ),

    path(
        'delete/<int:pk>/',
        EmployeeDeleteView.as_view(),
        name='employee_delete'
    ),

    path(
        'slow/',
        slow_view,
        name='slow'
    ),

]