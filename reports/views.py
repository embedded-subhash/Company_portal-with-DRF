import os

from django.core.files.base import ContentFile
from django.http import FileResponse, Http404, HttpResponse
from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView

from employees.permissions import IsAdminOrHR

from . import report_builder
from .models import GeneratedReport
from .serializers import GeneratedReportSerializer, ReportGenerateRequestSerializer


class ReportViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Module 10 (generate reports) + Module 11 (report download API).
    Only Admin/HR can generate and download business reports.
    """
    queryset = GeneratedReport.objects.all()
    serializer_class = GeneratedReportSerializer
    permission_classes = [IsAdminOrHR]
    filterset_fields = ["report_type", "format"]

    @action(detail=False, methods=["post"], url_path="generate")
    def generate(self, request):
        req = ReportGenerateRequestSerializer(data=request.data)
        req.is_valid(raise_exception=True)
        report_type = req.validated_data["report_type"]
        fmt = req.validated_data["format"]

        builder = report_builder.REPORT_BUILDERS.get((report_type, fmt))
        if builder is None:
            return Response(
                {"detail": f"'{fmt}' is not supported for report type '{report_type}'."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        build_fn, _content_type, ext = builder
        content = build_fn()

        report = GeneratedReport(report_type=report_type, format=fmt, generated_by=request.user)
        filename = f"{report_type}_{timezone.now():%Y%m%d_%H%M%S}.{ext}"
        report.file.save(filename, ContentFile(content), save=True)

        return Response(GeneratedReportSerializer(report).data, status=status.HTTP_201_CREATED)

    # -------------------- Module 11: Report Download API --------------------
    @action(detail=True, methods=["get"], url_path="download")
    def download(self, request, pk=None):
        report = self.get_object()
        if not report.file or not os.path.exists(report.file.path):
            raise Http404("Report file does not exist on the server.")
        _build_fn, content_type, _ext = report_builder.REPORT_BUILDERS[(report.report_type, report.format)]
        response = FileResponse(
            report.file.open("rb"), as_attachment=True, filename=os.path.basename(report.file.name)
        )
        response["Content-Type"] = content_type
        return response


class DashboardView(APIView):
    """Module 12: Dashboard Reports."""
    permission_classes = [IsAdminOrHR]

    def get(self, request):
        return Response(report_builder.dashboard_data())


class DashboardExportView(APIView):
    """Export dashboard as Excel or PDF (Module 12)."""
    permission_classes = [IsAdminOrHR]

    def get(self, request):
        fmt = request.query_params.get("file_format", "PDF").upper()
        builder = report_builder.REPORT_BUILDERS.get(("DASHBOARD", fmt))
        if builder is None:
            return Response({"detail": "format must be PDF or EXCEL."}, status=status.HTTP_400_BAD_REQUEST)
        build_fn, content_type, ext = builder
        content = build_fn()
        response = HttpResponse(content, content_type=content_type)
        response["Content-Disposition"] = f'attachment; filename="dashboard_{timezone.now():%Y%m%d}.{ext}"'
        return response
