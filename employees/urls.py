from django.urls import path

from .views import (
    EmployeeCreateView,
    EmployeeListView,
    EmployeeDetailView,
    EmployeeUpdateView,
    EmployeeDeleteView,
    TopEmployeesView,
    DepartmentEmployeeCountView,
    MonthlySalaryStatisticsView,
    EmployeesJoinedThisMonthView,
)


urlpatterns = [
    path(
        '',
        EmployeeListView.as_view(),
        name='employee_list'
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
        'reports/top-employees/',
        TopEmployeesView.as_view(),
        name='top_employees'
    ),

    path(
        'reports/department-count/',
        DepartmentEmployeeCountView.as_view(),
        name='department_employee_count'
    ),

    path(
        'reports/monthly-salary/',
        MonthlySalaryStatisticsView.as_view(),
        name='monthly_salary_statistics'
    ),

    path(
        'reports/joined-this-month/',
        EmployeesJoinedThisMonthView.as_view(),
        name='employees_joined_this_month'
    ),
]