from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from api.filters import EmployeeFilter
from api.pagination import EmployeeListPagination
from api.permissions import EmployeeAccessPolicy
from api.responses import SuccessResponse
from employees.models import Employee

from .serializers import EmployeeSerializerV2


class EmployeeViewSetV2(viewsets.ReadOnlyModelViewSet):
    """
    v2 read endpoint with richer employee data: department, manager,
    skills, and a flattened profile block.

    GET /api/v2/employees/
    GET /api/v2/employees/{id}/
    """

    queryset = Employee.objects.select_related("department", "manager").prefetch_related("skills").all()
    serializer_class = EmployeeSerializerV2
    pagination_class = EmployeeListPagination
    permission_classes = [IsAuthenticated, EmployeeAccessPolicy]

    filterset_class = EmployeeFilter
    search_fields = ["employee_id", "first_name", "last_name", "email", "phone"]
    ordering_fields = ["salary", "joining_date", "first_name", "created_at"]

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        profile = getattr(user, "profile", None)
        if profile and profile.role == "employee" and not user.is_superuser:
            qs = qs.filter(user=user)
        return qs

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
