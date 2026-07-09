import os

from django.http import FileResponse, Http404
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from employees.permissions import IsAdminOrHR, IsEmployeeReadOnlySelf

from .models import EmployeeDocument
from .serializers import EmployeeDocumentSerializer


class EmployeeDocumentViewSet(viewsets.ModelViewSet):
    """
    Module 2 (Upload/Download/Delete/List) + Module 11 (File Download API).
    HR/Admin: full access to all documents.
    Employees: can list/upload/download/delete only their own documents.
    """
    queryset = EmployeeDocument.objects.select_related("employee", "uploaded_by").all()
    serializer_class = EmployeeDocumentSerializer
    filterset_fields = ["employee", "document_type"]

    def get_permissions(self):
        return [IsAuthenticated(), IsEmployeeReadOnlySelf()]

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        if user.is_superuser or user.groups.filter(name__in=["Admin", "HR"]).exists():
            return qs
        return qs.filter(employee__user=user)

    def perform_create(self, serializer):
        serializer.save(uploaded_by=self.request.user)

    # -------------------- Module 11: File Download API --------------------
    @action(detail=True, methods=["get"], url_path="download")
    def download(self, request, pk=None):
        document = self.get_object()  # runs object-level permission check
        if not document.file or not os.path.exists(document.file.path):
            raise Http404("File does not exist on the server.")
        response = FileResponse(
            document.file.open("rb"),
            as_attachment=True,
            filename=os.path.basename(document.file.name),
        )
        response["Content-Type"] = "application/pdf"
        return response
