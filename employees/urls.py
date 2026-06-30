from django.urls import path

from .views import (
    EmployeeCreateView,
    EmployeeListView,
    EmployeeDetailView,
    EmployeeUpdateView,
    EmployeeDeleteView,
    EmployeeImportView,
    TaskStatusView,
)

urlpatterns = [

    path(
        "",
        EmployeeListView.as_view(),
        name="employee_list"
    ),

    path(
        "create/",
        EmployeeCreateView.as_view(),
        name="employee_create"
    ),

    path(
        "<int:pk>/",
        EmployeeDetailView.as_view(),
        name="employee_detail"
    ),

    path(
        "<int:pk>/update/",
        EmployeeUpdateView.as_view(),
        name="employee_update"
    ),

    path(
        "<int:pk>/delete/",
        EmployeeDeleteView.as_view(),
        name="employee_delete"
    ),

    path(
        "import/",
        EmployeeImportView.as_view(),
        name="employee_import"
    ),

    path(
        "tasks/<str:task_id>/",
        TaskStatusView.as_view(),
        name="task_status"
    ),
]