from django import forms
from django.contrib.auth.models import Group
from .models import User
import re


class UserRegistrationForm(forms.ModelForm):

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control'
            }
        )
    )

    confirm_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control'
            }
        )
    )

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'email',
            'phone',
            'employee_id',
            'role',
            'password',
            'confirm_password'
        ]

    def clean_email(self):

        email = self.cleaned_data.get('email')

        if User.objects.filter(email=email).exists():

            raise forms.ValidationError(
                "Email already exists."
            )

        return email

    def clean_employee_id(self):

        employee_id = self.cleaned_data.get(
            'employee_id'
        )

        pattern = r'^EMP\d+$'

        if not re.match(
            pattern,
            employee_id
        ):

            raise forms.ValidationError(
                "Employee ID must be like EMP001"
            )

        if User.objects.filter(
            employee_id=employee_id
        ).exists():

            raise forms.ValidationError(
                "Employee ID already exists."
            )

        return employee_id

    def clean_password(self):

        password = self.cleaned_data.get(
            'password'
        )

        if len(password) < 8:

            raise forms.ValidationError(
                "Password must be at least 8 characters."
            )

        if not re.search(
            r'[A-Z]',
            password
        ):

            raise forms.ValidationError(
                "Password must contain at least one uppercase letter."
            )

        if not re.search(
            r'[a-z]',
            password
        ):

            raise forms.ValidationError(
                "Password must contain at least one lowercase letter."
            )

        if not re.search(
            r'[0-9]',
            password
        ):

            raise forms.ValidationError(
                "Password must contain at least one number."
            )

        if not re.search(
            r'[@$!%*?&]',
            password
        ):

            raise forms.ValidationError(
                "Password must contain at least one special character."
            )

        return password

    def clean(self):

        cleaned_data = super().clean()

        password = cleaned_data.get(
            'password'
        )

        confirm_password = cleaned_data.get(
            'confirm_password'
        )

        if (
            password and
            confirm_password and
            password != confirm_password
        ):

            raise forms.ValidationError(
                "Passwords do not match."
            )

        return cleaned_data

    def save(self, commit=True):

        user = super().save(commit=False)

        user.set_password(
            self.cleaned_data['password']
        )

        if commit:

            user.save()

            role = user.role

            if role == 'ADMIN':
                group_name = 'Admin'

            elif role == 'HR':
                group_name = 'HR'

            elif role == 'MANAGER':
                group_name = 'Manager'

            else:
                group_name = 'Employee'

            group, created = Group.objects.get_or_create(
                name=group_name
            )

            user.groups.add(group)

        return user


class LoginForm(forms.Form):

    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control'
            }
        )
    )

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control'
            }
        )
    )