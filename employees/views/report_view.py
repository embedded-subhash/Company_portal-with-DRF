# employees/views/report_view.py

from rest_framework.response import Response
from rest_framework.views import APIView

from employees.services.report_service import ReportService


class TopEmployeesView(APIView):

    def get(self, request):

        employees = ReportService.top_10_highest_paid_employees()

        data = [
            {
                "employee_id": emp.employee_id,
                "first_name": emp.first_name,
                "last_name": emp.last_name,
                "salary": emp.salary
            }
            for emp in employees
        ]

        return Response(data)


class DepartmentEmployeeCountView(APIView):

    def get(self, request):

        departments = ReportService.department_wise_employee_count()

        data = [
            {
                "department": dept.name,
                "employee_count": dept.employee_count
            }
            for dept in departments
        ]

        return Response(data)


class MonthlySalaryStatisticsView(APIView):

    def get(self, request):

        statistics = ReportService.monthly_salary_statistics()

        return Response(statistics)


class EmployeesJoinedThisMonthView(APIView):

    def get(self, request):

        employees = ReportService.employees_joined_this_month()

        data = [
            {
                "employee_id": emp.employee_id,
                "first_name": emp.first_name,
                "last_name": emp.last_name,
                "joining_date": emp.joining_date
            }
            for emp in employees
        ]

        return Response(data)
    
class DepartmentEmployeesView(APIView):

    def get(self, request):

        departments = (
            ReportService.department_employee_report()
        )

        data = []

        for dept in departments:

            employees = [
                emp.first_name
                for emp in dept.employee_set.all()
            ]

            data.append({
                "department": dept.name,
                "employees": employees
            })

        return Response(data)