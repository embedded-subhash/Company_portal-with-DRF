from employees.models import Employee


class OptimizationService:

    @staticmethod
    def employee_with_department():

        return Employee.objects.select_related(
            "department"
        )

    @staticmethod
    def employee_names_only():

        return Employee.objects.only(
            "first_name",
            "last_name"
        )

    @staticmethod
    def employees_without_images():

        return Employee.objects.defer(
            "profile_image"
        )