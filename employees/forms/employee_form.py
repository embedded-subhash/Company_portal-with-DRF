from django import forms
from employees.models import Employee
from datetime import date
import re
class EmployeeForm(forms.ModelForm):

    class Meta:
        model = Employee
        fields = "__all__"

    def clean_employee_id(self):

        employee_id = self.cleaned_data["employee_id"]

        pattern = r"^EMP\d+$"

        if not re.match(pattern, employee_id):

            raise forms.ValidationError(
                "Employee ID must be like EMP001"
            )

        return employee_id

    def clean_email(self):

        email = self.cleaned_data["email"]

        qs = Employee.objects.filter(
            email=email
        )

        if self.instance.pk:

            qs = qs.exclude(
                pk=self.instance.pk
            )

        if qs.exists():

            raise forms.ValidationError(
                "Email already exists"
            )

        return email

    def clean_phone(self):

        phone = self.cleaned_data["phone"]

        if not phone.isdigit() or len(phone) != 10:

            raise forms.ValidationError(
                "Phone must contain 10 digits"
            )

        return phone

    def clean_salary(self):

        salary = self.cleaned_data["salary"]

        if salary < 10000:

            raise forms.ValidationError(
                "Minimum salary is 10000"
            )

        if salary > 500000:

            raise forms.ValidationError(
                "Maximum salary is 500000"
            )

        return salary

    def clean_joining_date(self):

        joining_date = self.cleaned_data["joining_date"]

        if joining_date > date.today():

            raise forms.ValidationError(
                "Future date not allowed"
            )

        return joining_date