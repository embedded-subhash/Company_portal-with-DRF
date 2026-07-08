from django.contrib.auth.models import User
from django.db import transaction
from django.db.models import Avg, Count, Q
from django.utils import timezone
from datetime import timedelta

from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from api.filters import EmployeeFilter
from api.pagination import DepartmentListPagination, EmployeeListPagination
from api.permissions import EmployeeAccessPolicy, IsAdmin
from api.responses import ErrorResponse, SuccessResponse
from departments.models import Department
from employees.models import Employee
from reports.models import AuditLog

from .serializers import (
    DashboardStatsSerializer,
    DepartmentSerializer,
    EmployeeSerializer,
    EmployeeListSerializer,
)


class DepartmentViewSet(viewsets.ModelViewSet):
    """Full CRUD for departments. 10 records per page."""

    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    pagination_class = DepartmentListPagination
    permission_classes = [IsAuthenticated, IsAdmin]
    filter_backends_search_fields = ["name", "code"]
    search_fields = ["name", "code"]
    ordering_fields = ["name", "created_at"]

    def get_permissions(self):
        # Anyone authenticated can read; only Admin can write.
        if self.request.method in ("GET", "HEAD", "OPTIONS"):
            return [IsAuthenticated()]
        return [IsAuthenticated(), IsAdmin()]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return ErrorResponse(errors=serializer.errors)
        self.perform_create(serializer)
        return SuccessResponse(
            message="Department Created Successfully", data=serializer.data, status=status.HTTP_201_CREATED
        )

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if not serializer.is_valid():
            return ErrorResponse(errors=serializer.errors)
        self.perform_update(serializer)
        return SuccessResponse(message="Department Updated Successfully", data=serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return SuccessResponse(message="Department Deleted Successfully", data={})

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page if page is not None else queryset, many=True)
        if page is not None:
            paginated = self.get_paginated_response(serializer.data)
            return SuccessResponse(message="Departments Fetched Successfully", data=paginated.data)
        return SuccessResponse(message="Departments Fetched Successfully", data=serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return SuccessResponse(message="Department Fetched Successfully", data=serializer.data)


class EmployeeViewSet(viewsets.ModelViewSet):
    """
    Employee CRUD + Search + Filter + Ordering + Pagination + Bulk ops.

    GET    /api/v1/employees/
    POST   /api/v1/employees/
    GET    /api/v1/employees/{id}/
    PUT    /api/v1/employees/{id}/
    PATCH  /api/v1/employees/{id}/
    DELETE /api/v1/employees/{id}/
    POST   /api/v1/employees/bulk-create/
    PATCH  /api/v1/employees/bulk-update/
    POST   /api/v1/employees/bulk-delete/
    """

    queryset = Employee.objects.select_related("department", "manager").all()
    serializer_class = EmployeeSerializer
    pagination_class = EmployeeListPagination
    permission_classes = [IsAuthenticated, EmployeeAccessPolicy]

    filterset_class = EmployeeFilter
    search_fields = ["employee_id", "first_name", "last_name", "email", "phone"]
    ordering_fields = ["salary", "joining_date", "first_name", "created_at"]
    ordering = ["-created_at"]

    def get_serializer_class(self):
        if self.action == "list":
            return EmployeeListSerializer
        return EmployeeSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        profile = getattr(user, "profile", None)
        # Employees may only ever see their own record.
        if profile and profile.role == "employee" and not user.is_superuser:
            qs = qs.filter(user=user)
        return qs

    # --- Standard CRUD wrapped in the standard response envelope ---------------
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page if page is not None else queryset, many=True)
        if page is not None:
            paginated = self.get_paginated_response(serializer.data)
            return SuccessResponse(message="Employees Fetched Successfully", data=paginated.data)
        return SuccessResponse(message="Employees Fetched Successfully", data=serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return SuccessResponse(message="Employee Fetched Successfully", data=serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return ErrorResponse(errors=serializer.errors)
        with transaction.atomic():
            self.perform_create(serializer)
            AuditLog.objects.create(
                user=request.user,
                action="Created Employee",
                details=f"Employee {serializer.data.get('employee_id')} created.",
            )
        return SuccessResponse(
            message="Employee Created Successfully", data=serializer.data, status=status.HTTP_201_CREATED
        )

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if not serializer.is_valid():
            return ErrorResponse(errors=serializer.errors)
        with transaction.atomic():
            self.perform_update(serializer)
            AuditLog.objects.create(
                user=request.user,
                action="Updated Employee",
                details=f"Employee {instance.employee_id} updated.",
            )
        return SuccessResponse(message="Employee Updated Successfully", data=serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        emp_id = instance.employee_id
        with transaction.atomic():
            instance.delete()
            AuditLog.objects.create(
                user=request.user, action="Deleted Employee", details=f"Employee {emp_id} deleted."
            )
        return SuccessResponse(message="Employee Deleted Successfully", data={})

    # --- Module 8: Bulk Operations --------------------------------------------
    @action(detail=False, methods=["post"], url_path="bulk-create")
    def bulk_create(self, request):
        """POST /api/v1/employees/bulk-create/  body: [{...}, {...}]"""
        items = request.data
        if not isinstance(items, list):
            return ErrorResponse(message="Validation Failed", errors={"detail": "Expected a list of employees."})

        serializer = EmployeeSerializer(data=items, many=True)
        if not serializer.is_valid():
            return ErrorResponse(message="Validation Failed", errors=serializer.errors)

        with transaction.atomic():
            created = serializer.save()
            AuditLog.objects.create(
                user=request.user, action="Bulk Created Employees", details=f"{len(created)} employees created."
            )

        return SuccessResponse(
            message="Employees Created Successfully",
            data=EmployeeSerializer(created, many=True).data,
            status=status.HTTP_201_CREATED,
        )

    @action(detail=False, methods=["patch", "put"], url_path="bulk-update")
    def bulk_update(self, request):
        """PATCH /api/v1/employees/bulk-update/  body: [{"id": 1, "salary": 60000}, ...]"""
        items = request.data
        if not isinstance(items, list):
            return ErrorResponse(message="Validation Failed", errors={"detail": "Expected a list of updates."})

        errors = {}
        updated_instances = []

        with transaction.atomic():
            for index, item in enumerate(items):
                emp_id = item.get("id")
                try:
                    instance = Employee.objects.select_for_update().get(pk=emp_id)
                except (Employee.DoesNotExist, TypeError, ValueError):
                    errors[index] = {"id": f"Employee with id {emp_id} does not exist."}
                    continue

                serializer = EmployeeSerializer(instance, data=item, partial=True)
                if not serializer.is_valid():
                    errors[index] = serializer.errors
                    continue

                serializer.save()
                updated_instances.append(serializer.data)

            if errors:
                # Roll back the whole batch if anything failed.
                transaction.set_rollback(True)
                return ErrorResponse(message="Validation Failed", errors=errors)

            AuditLog.objects.create(
                user=request.user,
                action="Bulk Updated Employees",
                details=f"{len(updated_instances)} employees updated.",
            )

        return SuccessResponse(message="Employees Updated Successfully", data=updated_instances)

    @action(detail=False, methods=["post"], url_path="bulk-delete")
    def bulk_delete(self, request):
        """POST /api/v1/employees/bulk-delete/  body: {"ids": [1, 2, 3]}"""
        ids = request.data.get("ids")
        if not isinstance(ids, list) or not ids:
            return ErrorResponse(message="Validation Failed", errors={"ids": "Provide a non-empty list of ids."})

        with transaction.atomic():
            queryset = Employee.objects.filter(pk__in=ids)
            found_ids = set(queryset.values_list("id", flat=True))
            missing = set(ids) - found_ids
            if missing:
                return ErrorResponse(
                    message="Validation Failed",
                    errors={"ids": f"No employees found for ids: {sorted(missing)}"},
                )
            deleted_count, _ = queryset.delete()
            AuditLog.objects.create(
                user=request.user, action="Bulk Deleted Employees", details=f"{deleted_count} employees deleted."
            )

        return SuccessResponse(message="Employees Deleted Successfully", data={"deleted_count": deleted_count})


class EmployeeProfileView(APIView):
    """
    GET/PUT/PATCH /api/v1/employees/profile/me/
    Every authenticated employee can view and update their own profile.
    """

    permission_classes = [IsAuthenticated]

    def get_object(self, request):
        try:
            return Employee.objects.select_related("department").get(user=request.user)
        except Employee.DoesNotExist:
            return None

    def get(self, request):
        instance = self.get_object(request)
        if instance is None:
            return ErrorResponse(message="Profile Not Found", errors={}, status=status.HTTP_404_NOT_FOUND)
        return SuccessResponse(message="Profile Fetched Successfully", data=EmployeeSerializer(instance).data)

    def patch(self, request):
        instance = self.get_object(request)
        if instance is None:
            return ErrorResponse(message="Profile Not Found", errors={}, status=status.HTTP_404_NOT_FOUND)
        serializer = EmployeeSerializer(instance, data=request.data, partial=True)
        if not serializer.is_valid():
            return ErrorResponse(message="Validation Failed", errors=serializer.errors)
        serializer.save()
        return SuccessResponse(message="Profile Updated Successfully", data=serializer.data)


class DashboardStatsView(APIView):
    """
    GET /api/v1/dashboard/stats/

    Returns: Total Employees, Active Employees, Department Count,
             New Joiners (last 30 days), Average Salary.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        thirty_days_ago = timezone.now().date() - timedelta(days=30)

        stats = {
            "total_employees": Employee.objects.count(),
            "active_employees": Employee.objects.filter(status=Employee.Status.ACTIVE).count(),
            "inactive_employees": Employee.objects.filter(status=Employee.Status.INACTIVE).count(),
            "department_count": Department.objects.count(),
            "new_joiners_last_30_days": Employee.objects.filter(joining_date__gte=thirty_days_ago).count(),
            "average_salary": Employee.objects.aggregate(avg=Avg("salary"))["avg"] or 0,
        }
        serializer = DashboardStatsSerializer(stats)
        return SuccessResponse(message="Dashboard Statistics Fetched Successfully", data=serializer.data)
