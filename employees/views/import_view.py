from django.contrib import messages
from django.shortcuts import redirect, render
from django.views import View

from employees.forms import EmployeeImportForm
from employees.services.import_service import EmployeeImportService


class EmployeeImportView(View):

    template_name = "employees/import.html"

    def get(self, request):

        form = EmployeeImportForm()

        return render(
            request,
            self.template_name,
            {"form": form}
        )

    def post(self, request):

        form = EmployeeImportForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            file = request.FILES["file"]

            result = EmployeeImportService.import_employees(file)

            messages.success(
                request,
                f'{result["imported_count"]} employees imported successfully.'
            )

            return redirect("employee_list")

        return render(
            request,
            self.template_name,
            {"form": form}
        )