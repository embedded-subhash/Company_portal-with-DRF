from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework.permissions import IsAuthenticated

from api.pagination import StandardPagination
from api.permissions import IsAdminHRManagerOrReadOnly
from api.serializers import EmployeeSerializer, EmployeeV2Serializer
from api.services.employee_service import EmployeeService
from api.throttling import EmployeeRateThrottle
from .mixins import StandardResponseModelViewSet


@method_decorator(cache_page(60 * 5), name="list")
class EmployeeV1ViewSet(StandardResponseModelViewSet):
    serializer_class = EmployeeSerializer
    permission_classes = [IsAuthenticated, IsAdminHRManagerOrReadOnly]
    throttle_classes = [EmployeeRateThrottle]
    pagination_class = StandardPagination
    create_message = "Employee Created Successfully"
    update_message = "Employee Updated Successfully"
    delete_message = "Employee Deleted Successfully"
    list_message = "Employees Fetched Successfully"
    retrieve_message = "Employee Fetched Successfully"
    search_fields = ["employee_id", "first_name", "last_name", "email"]
    ordering_fields = ["id", "employee_id", "first_name", "joining_date", "salary"]
    filterset_fields = ["department", "status"]

    def get_queryset(self):
        return EmployeeService.list_employees()

    def perform_service_create(self, validated_data):
        return EmployeeService.create_employee(validated_data)

    def perform_service_update(self, instance, validated_data):
        return EmployeeService.update_employee(instance, validated_data)

    def perform_service_delete(self, instance):
        return EmployeeService.delete_employee(instance)


@method_decorator(cache_page(60 * 5), name="list")
class EmployeeV2ViewSet(StandardResponseModelViewSet):
    serializer_class = EmployeeV2Serializer
    permission_classes = [IsAuthenticated, IsAdminHRManagerOrReadOnly]
    throttle_classes = [EmployeeRateThrottle]
    pagination_class = StandardPagination
    create_message = "Employee Created Successfully"
    update_message = "Employee Updated Successfully"
    delete_message = "Employee Deleted Successfully"
    list_message = "Employees Fetched Successfully"
    retrieve_message = "Employee Fetched Successfully"
    search_fields = ["employee_id", "first_name", "last_name", "email"]
    ordering_fields = ["id", "employee_id", "first_name", "joining_date", "salary"]
    filterset_fields = ["department", "status"]

    def get_queryset(self):
        return EmployeeService.list_employees()

    def perform_service_create(self, validated_data):
        return EmployeeService.create_employee(validated_data)

    def perform_service_update(self, instance, validated_data):
        return EmployeeService.update_employee(instance, validated_data)

    def perform_service_delete(self, instance):
        return EmployeeService.delete_employee(instance)
