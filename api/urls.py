from django.urls import path
from . import views

urlpatterns = [

    path(
        'employees/',
        views.EmployeeListCreateAPIView.as_view(),
        name='employee_list_create'
    ),

    path(
        'employees/<int:pk>/',
        views.EmployeeDetailAPIView.as_view(),
        name='employee_detail'
    ),
]