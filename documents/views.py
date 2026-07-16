import os

from django.http import FileResponse, Http404
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from employees.permissions import IsEmployeeReadOnlySelf
from .models import EmployeeDocument
from .serializers import EmployeeDocumentSerializer


class EmployeeDocumentViewSet(viewsets.ModelViewSet):
    """
    Employee Document Management

    APIs
    ----
    GET     /api/v1/documents/
    POST    /api/v1/documents/
    GET     /api/v1/documents/<id>/
    PUT     /api/v1/documents/<id>/
    PATCH   /api/v1/documents/<id>/
    DELETE  /api/v1/documents/<id>/
    GET     /api/v1/documents/<id>/download/
    """

    queryset = EmployeeDocument.objects.select_related(
        "employee",
        "uploaded_by"
    ).all()

    serializer_class = EmployeeDocumentSerializer
    permission_classes = [IsAuthenticated, IsEmployeeReadOnlySelf]

    filterset_fields = [
        "employee",
        "document_type",
    ]

    def get_queryset(self):
        user = self.request.user

        if (
            user.is_superuser
            or user.groups.filter(name__in=["Admin", "HR"]).exists()
        ):
            return self.queryset

        return self.queryset.filter(employee__user=user)

    def perform_create(self, serializer):
        serializer.save(uploaded_by=self.request.user)

    @action(detail=True, methods=["get"])
    def download(self, request, pk=None):

        document = self.get_object()

        if not document.file:
            raise Http404("No file attached.")

        if not os.path.exists(document.file.path):
            raise Http404("File not found.")

        return FileResponse(
            document.file.open("rb"),
            as_attachment=True,
            filename=os.path.basename(document.file.name),
        )