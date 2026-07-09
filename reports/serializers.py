from rest_framework import serializers

from .models import GeneratedReport


class GeneratedReportSerializer(serializers.ModelSerializer):
    generated_by_username = serializers.CharField(source="generated_by.username", read_only=True)

    class Meta:
        model = GeneratedReport
        fields = ["id", "report_type", "format", "file", "generated_by", "generated_by_username", "generated_at"]
        read_only_fields = ["file", "generated_by", "generated_at"]


class ReportGenerateRequestSerializer(serializers.Serializer):
    report_type = serializers.ChoiceField(choices=["EMPLOYEE", "DEPARTMENT", "SALARY", "ATTENDANCE", "DASHBOARD"])
    format = serializers.ChoiceField(choices=["PDF", "EXCEL", "CSV"])
