from departments.models import Department


class DepartmentService:

    @staticmethod
    def department_employee_report():

        return Department.objects.prefetch_related(
            "employee_set"
        )