from django import forms


class EmployeeImportForm(forms.Form):

    file = forms.FileField(
        label="Upload Excel File"
    )