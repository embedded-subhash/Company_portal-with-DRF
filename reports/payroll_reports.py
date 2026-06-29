from django.db import connection


def monthly_payroll_report(month):

    with connection.cursor() as cursor:

        cursor.execute("""
            SELECT
                e.employee_id,
                e.first_name,
                p.month,
                p.net_salary
            FROM payroll_payroll p
            INNER JOIN employees_employee e
            ON p.employee_id = e.id
            WHERE p.month = %s
        """, [month])

        return cursor.fetchall()