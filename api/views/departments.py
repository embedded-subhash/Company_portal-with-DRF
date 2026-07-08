from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework.permissions import IsAuthenticated

from api.permissions import IsAdminOnly
from api.serializers import DepartmentSerializer
from api.services.department_service import DepartmentService
from .mixins import StandardResponseModelViewSet


@method_decorator(cache_page(60 * 5), name="list")
class DepartmentViewSet(StandardResponseModelViewSet):
    serializer_class = DepartmentSerializer
    permission_classes = [IsAuthenticated, IsAdminOnly]
    create_message = "Department Created Successfully"
    update_message = "Department Updated Successfully"
    delete_message = "Department Deleted Successfully"
    list_message = "Departments Fetched Successfully"
    retrieve_message = "Department Fetched Successfully"
    search_fields = ["name"]
    ordering_fields = ["id", "name", "created_at"]

    def get_queryset(self):
        return DepartmentService.list_departments()

    def perform_service_create(self, validated_data):
        return DepartmentService.create_department(validated_data)

    def perform_service_update(self, instance, validated_data):
        return DepartmentService.update_department(instance, validated_data)

    def perform_service_delete(self, instance):
        return DepartmentService.delete_department(instance)
