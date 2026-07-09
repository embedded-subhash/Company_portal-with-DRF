from datetime import date

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.http import HttpResponse, FileResponse
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from reports import csv_handler, excel_export, pdf_generator, qr_generator
from .models import Attendance, Department, Employee
from .permissions import IsAdminOrHR, IsEmployeeReadOnlySelf
from .serializers import (
    AttendanceSerializer,
    DepartmentSerializer,
    EmployeeSelfServiceSerializer,
    EmployeeSerializer,
    ExcelImportResultSerializer,
)


class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [IsAdminOrHR]


class EmployeeViewSet(viewsets.ModelViewSet):
    """
    Full CRUD for HR/Admin. Employees hitting their own record get a
    restricted read-mostly view (enforced via get_serializer_class + object perm).
    """
    queryset = Employee.objects.select_related("department").all()
    filterset_fields = ["department", "status", "designation"]
    search_fields = ["employee_id", "first_name", "last_name", "email"]

    def get_permissions(self):
        if self.action in ("list", "create", "destroy", "import_excel", "export_excel", "export_csv"):
            return [IsAdminOrHR()]
        return [IsAuthenticated(), IsEmployeeReadOnlySelf()]

    def get_serializer_class(self):
        user = self.request.user
        if user.is_authenticated and not (user.is_superuser or user.groups.filter(name__in=["Admin", "HR"]).exists()):
            return EmployeeSelfServiceSerializer
        return EmployeeSerializer

    # -------------------- Module 3: Excel Import --------------------
    @action(detail=False, methods=["post"], url_path="import")
    def import_excel(self, request):
        file_obj = request.FILES.get("file")
        if not file_obj:
            return Response({"detail": "No file uploaded."}, status=status.HTTP_400_BAD_REQUEST)
        result = excel_export.import_employees_from_excel(file_obj)
        return Response(ExcelImportResultSerializer(result).data, status=status.HTTP_201_CREATED)

    # -------------------- Module 4: Excel Export --------------------
    @action(detail=False, methods=["get"], url_path="export")
    def export_excel(self, request):
        export_type = request.query_params.get("type", "employees")
        builders = {
            "employees": (excel_export.export_employee_list_excel, self.filter_queryset(self.get_queryset()), "employee_list.xlsx"),
            "departments": (excel_export.export_department_list_excel, Department.objects.all(), "department_list.xlsx"),
            "salary": (excel_export.export_salary_report_excel, self.filter_queryset(self.get_queryset()), "salary_report.xlsx"),
            "attendance": (excel_export.export_attendance_report_excel, Attendance.objects.select_related("employee"), "attendance_report.xlsx"),
        }
        if export_type not in builders:
            return Response({"detail": f"Unknown export type '{export_type}'."}, status=status.HTTP_400_BAD_REQUEST)
        builder_fn, queryset, filename = builders[export_type]
        content = builder_fn(queryset)
        response = HttpResponse(content, content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        response["Content-Disposition"] = f'attachment; filename="{filename}"'
        return response

    # -------------------- Module 5: CSV Import/Export --------------------
    @action(detail=False, methods=["post"], url_path="import-csv")
    def import_csv(self, request):
        file_obj = request.FILES.get("file")
        if not file_obj:
            return Response({"detail": "No file uploaded."}, status=status.HTTP_400_BAD_REQUEST)
        result = csv_handler.parse_employee_csv(file_obj)
        return Response(ExcelImportResultSerializer(result).data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=["get"], url_path="export-csv")
    def export_csv(self, request):
        content = csv_handler.build_employee_csv(self.filter_queryset(self.get_queryset()))
        response = HttpResponse(content, content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="employee_list.csv"'
        return response

    # -------------------- Module 6: Employee Profile PDF --------------------
    @action(detail=True, methods=["get"], url_path="profile-pdf")
    def profile_pdf(self, request, pk=None):
        employee = self.get_object()
        content = pdf_generator.generate_employee_profile_pdf(employee)
        response = HttpResponse(content, content_type="application/pdf")
        response["Content-Disposition"] = f'attachment; filename="{employee.employee_id}_Profile.pdf"'
        return response

    # -------------------- Module 7: Salary Slip PDF --------------------
    @action(detail=True, methods=["get"], url_path="salary-slip")
    def salary_slip(self, request, pk=None):
        employee = self.get_object()
        month = request.query_params.get("month", date.today().strftime("%B"))
        year = int(request.query_params.get("year", date.today().year))
        content = pdf_generator.generate_salary_slip_pdf(employee, month, year)
        response = HttpResponse(content, content_type="application/pdf")
        response["Content-Disposition"] = f'attachment; filename="SalarySlip_{month}_{year}_{employee.employee_id}.pdf"'
        return response

    # -------------------- Module 8: QR Code --------------------
    @action(detail=True, methods=["get"], url_path="qr-code")
    def qr_code(self, request, pk=None):
        employee = self.get_object()
        content = qr_generator.generate_employee_qr_png_bytes(employee)
        response = HttpResponse(content, content_type="image/png")
        response["Content-Disposition"] = f'inline; filename="{employee.employee_id}_QR.png"'
        return response

    # -------------------- Module 9: Employee ID Card --------------------
    @action(detail=True, methods=["get"], url_path="id-card")
    def id_card(self, request, pk=None):
        employee = self.get_object()
        valid_till = date(date.today().year + 1, date.today().month, 1)
        content = pdf_generator.generate_employee_id_card_pdf(employee, valid_till)

        # Persist a copy under media/id_cards/ (Module 9 output folder)
        filename = f"id_cards/ID_{employee.employee_id}.pdf"
        if default_storage.exists(filename):
            default_storage.delete(filename)
        default_storage.save(filename, ContentFile(content))

        response = HttpResponse(content, content_type="application/pdf")
        response["Content-Disposition"] = f'attachment; filename="ID_{employee.employee_id}.pdf"'
        return response

    def get_object(self):
        obj = super().get_object()
        self.check_object_permissions(self.request, obj)
        return obj


class AttendanceViewSet(viewsets.ModelViewSet):
    queryset = Attendance.objects.select_related("employee").all()
    serializer_class = AttendanceSerializer
    permission_classes = [IsAdminOrHR]
    filterset_fields = ["employee", "status", "date"]
