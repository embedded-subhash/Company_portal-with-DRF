from django.conf import settings
from django.db import models

REPORT_TYPE_CHOICES = (
    ("EMPLOYEE", "Employee Report"),
    ("DEPARTMENT", "Department Report"),
    ("SALARY", "Salary Report"),
    ("ATTENDANCE", "Attendance Report"),
    ("DASHBOARD", "Dashboard Report"),
)

FORMAT_CHOICES = (
    ("PDF", "PDF"),
    ("EXCEL", "Excel"),
    ("CSV", "CSV"),
)


def report_file_path(instance, filename):
    return f"reports/{instance.report_type.lower()}/{filename}"


class GeneratedReport(models.Model):
    report_type = models.CharField(max_length=20, choices=REPORT_TYPE_CHOICES)
    format = models.CharField(max_length=10, choices=FORMAT_CHOICES)
    file = models.FileField(upload_to=report_file_path)
    generated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="generated_reports"
    )
    generated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-generated_at"]

    def __str__(self):
        return f"{self.report_type} ({self.format}) - {self.generated_at:%Y-%m-%d %H:%M}"
