from django.urls import path
from employees.views.task_views import TaskStatusView


urlpatterns = [
    path(
        "tasks/<str:task_id>/",
        TaskStatusView.as_view(),
        name="task-status"
    ),
]