from datetime import timedelta

from django.db import transaction
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from api.filters import EmployeeFilter
from api.pagination import EmployeeListPagination, StandardPagination
from api.permissions import EmployeeAccessPolicy
from api.responses import ErrorResponse, SuccessResponse
from api.serializers import EmployeeSerializer, EmployeeV2Serializer
from api.services.employee_service import EmployeeService
from api.throttling import EmployeeRateThrottle
from departments.models import Department
from employees.models import Employee
from .mixins import StandardResponseModelViewSet


@method_decorator(cache_page(60 * 5), name='list')
class EmployeeV1ViewSet(StandardResponseModelViewSet):
    serializer_class = EmployeeSerializer
    permission_classes = [IsAuthenticated, EmployeeAccessPolicy]
    throttle_classes = [EmployeeRateThrottle]
    pagination_class = EmployeeListPagination
    create_message = 'Employee Created Successfully'
    update_message = 'Employee Updated Successfully'
    delete_message = 'Employee Deleted Successfully'
    list_message = 'Employees Fetched Successfully'
    retrieve_message = 'Employee Fetched Successfully'
    search_fields = ['employee_id', 'first_name', 'last_name', 'email', 'phone']
    ordering_fields = ['salary', 'joining_date', 'first_name', 'created_at']
    filterset_class = EmployeeFilter
    ordering = ['-created_at']

    def get_queryset(self):
        return EmployeeService.list_employees()

    def perform_service_create(self, validated_data):
        return EmployeeService.create_employee(validated_data)

    def perform_service_update(self, instance, validated_data):
        return EmployeeService.update_employee(instance, validated_data)

    def perform_service_delete(self, instance):
        return EmployeeService.delete_employee(instance)

    @action(detail=False, methods=['post'], url_path='bulk-create')
    def bulk_create(self, request):
        items = request.data
        if not isinstance(items, list):
            return ErrorResponse(message='Validation Failed', errors={'detail': 'Expected a list of employees.'})

        serializer = EmployeeSerializer(data=items, many=True)
        if not serializer.is_valid():
            return ErrorResponse(message='Validation Failed', errors=serializer.errors)

        with transaction.atomic():
            created = serializer.save()

        return SuccessResponse(message='Employees Created Successfully', data=EmployeeSerializer(created, many=True).data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['patch', 'put'], url_path='bulk-update')
    def bulk_update(self, request):
        items = request.data
        if not isinstance(items, list):
            return ErrorResponse(message='Validation Failed', errors={'detail': 'Expected a list of updates.'})

        errors = {}
        for index, item in enumerate(items):
            emp_id = item.get('id')
            try:
                instance = Employee.objects.get(pk=emp_id)
            except (Employee.DoesNotExist, TypeError, ValueError):
                errors[index] = {'id': f'Employee with id {emp_id} does not exist.'}
                continue

            serializer = EmployeeSerializer(instance, data=item, partial=True)
            if not serializer.is_valid():
                errors[index] = serializer.errors
                continue
            serializer.save()

        if errors:
            return ErrorResponse(message='Validation Failed', errors=errors)

        return SuccessResponse(message='Employees Updated Successfully', data=items)

    @action(detail=False, methods=['post'], url_path='bulk-delete')
    def bulk_delete(self, request):
        ids = request.data.get('ids')
        if not isinstance(ids, list) or not ids:
            return ErrorResponse(message='Validation Failed', errors={'ids': 'Provide a non-empty list of ids.'})

        with transaction.atomic():
            queryset = Employee.objects.filter(pk__in=ids)
            found_ids = set(queryset.values_list('id', flat=True))
            missing = set(ids) - found_ids
            if missing:
                return ErrorResponse(message='Validation Failed', errors={'ids': f'No employees found for ids: {sorted(missing)}'})
            deleted_count, _ = queryset.delete()

        return SuccessResponse(message='Employees Deleted Successfully', data={'deleted_count': deleted_count})

    @action(detail=False, methods=['get'], url_path='dashboard-stats')
    def dashboard_stats(self, request):
        thirty_days_ago = timezone.now().date() - timedelta(days=30)
        stats = {
            'total_employees': Employee.objects.count(),
            'active_employees': Employee.objects.filter(status=True).count(),
            'inactive_employees': Employee.objects.filter(status=False).count(),
            'department_count': Department.objects.count(),
            'new_joiners_last_30_days': Employee.objects.filter(joining_date__gte=thirty_days_ago).count(),
            'average_salary': Employee.objects.aggregate(avg=models.Avg('salary'))['avg'] or 0,
        }
        return SuccessResponse(message='Dashboard Statistics Fetched Successfully', data=stats)


@method_decorator(cache_page(60 * 5), name='list')
class EmployeeV2ViewSet(StandardResponseModelViewSet):
    serializer_class = EmployeeV2Serializer
    permission_classes = [IsAuthenticated, EmployeeAccessPolicy]
    throttle_classes = [EmployeeRateThrottle]
    pagination_class = StandardPagination
    create_message = 'Employee Created Successfully'
    update_message = 'Employee Updated Successfully'
    delete_message = 'Employee Deleted Successfully'
    list_message = 'Employees Fetched Successfully'
    retrieve_message = 'Employee Fetched Successfully'
    search_fields = ['employee_id', 'first_name', 'last_name', 'email', 'phone']
    ordering_fields = ['salary', 'joining_date', 'first_name', 'created_at']
    filterset_class = EmployeeFilter
    ordering = ['-created_at']

    def get_queryset(self):
        return EmployeeService.list_employees()

    def perform_service_create(self, validated_data):
        return EmployeeService.create_employee(validated_data)

    def perform_service_update(self, instance, validated_data):
        return EmployeeService.update_employee(instance, validated_data)

    def perform_service_delete(self, instance):
        return EmployeeService.delete_employee(instance)
