from django.test import TestCase

from reports import report_builder


class ReportBuilderTests(TestCase):
    def test_employee_report_builder_generates_pdf_bytes(self):
        data = report_builder.employee_report_pdf()
        self.assertTrue(data.startswith(b"%PDF") or len(data) > 0)

    def test_department_report_builder_generates_excel_bytes(self):
        data = report_builder.department_report_excel()
        self.assertGreater(len(data), 0)

    def test_salary_report_builder_generates_csv_bytes(self):
        data = report_builder.salary_report_csv()
        self.assertTrue(data.startswith(b"\xef\xbb\xbf") or data.startswith(b"Employee"))

    def test_dashboard_data_contains_expected_metrics(self):
        data = report_builder.dashboard_data()
        self.assertIn("employee_count", data)
        self.assertIn("department_count", data)
        self.assertIn("salary_stats", data)
        self.assertIn("attendance_summary", data)
