from django.db import connection
from django.db.models import Avg, Count, Max, Min

from employees.models import Employee
from departments.models import Department


def top_10_employees():

    return Employee.objects.order_by(
        '-salary'
    )[:10]


def employee_statistics():

    return Employee.objects.aggregate(
        average_salary=Avg('salary'),
        highest_salary=Max('salary'),
        lowest_salary=Min('salary')
    )


def department_summary():

    return Department.objects.annotate(
        total_employees=Count('employee'),
        average_salary=Avg('employee__salary')
    )


def raw_top_salary_report():

    with connection.cursor() as cursor:

        cursor.execute("""
            SELECT
                employee_id,
                first_name,
                last_name,
                salary
            FROM employees_employee
            ORDER BY salary DESC
            LIMIT 10
        """)

        return cursor.fetchall()