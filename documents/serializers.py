from rest_framework import serializers

from .models import EmployeeDocument


class EmployeeDocumentSerializer(serializers.ModelSerializer):
    employee_name = serializers.CharField(source="employee.full_name", read_only=True)
    uploaded_by_username = serializers.CharField(source="uploaded_by.username", read_only=True)
    file_url = serializers.SerializerMethodField()

    class Meta:
        model = EmployeeDocument
        fields = [
            "id", "employee", "employee_name", "document_name", "document_type",
            "file", "file_url", "uploaded_by", "uploaded_by_username", "uploaded_at",
        ]
        read_only_fields = ["uploaded_by", "uploaded_at"]

    def get_file_url(self, obj):
        request = self.context.get("request")
        if obj.file and request:
            return request.build_absolute_uri(obj.file.url)
        return obj.file.url if obj.file else None
