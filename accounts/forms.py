from django import forms
from django.contrib.auth.models import Group
from .models import User
import re


class UserRegistrationForm(forms.ModelForm):

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
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

    # ---------------- EMAIL VALIDATION ----------------
    def clean_email(self):
        email = self.cleaned_data.get('email')

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exists.")

        return email

    # ---------------- EMPLOYEE ID VALIDATION ----------------
    def clean_employee_id(self):
        employee_id = self.cleaned_data.get('employee_id')

        pattern = r'^EMP\d+$'

        if not re.match(pattern, employee_id):
            raise forms.ValidationError("Employee ID must be like EMP001")

        if User.objects.filter(employee_id=employee_id).exists():
            raise forms.ValidationError("Employee ID already exists.")

        return employee_id

    # ---------------- PASSWORD VALIDATION ----------------
    def clean_password(self):
        password = self.cleaned_data.get('password')

        if len(password) < 8:
            raise forms.ValidationError("Password must be at least 8 characters.")

        if not re.search(r'[A-Z]', password):
            raise forms.ValidationError("Must contain at least one uppercase letter.")

        if not re.search(r'[a-z]', password):
            raise forms.ValidationError("Must contain at least one lowercase letter.")

        if not re.search(r'[0-9]', password):
            raise forms.ValidationError("Must contain at least one number.")

        if not re.search(r'[@$!%*?&]', password):
            raise forms.ValidationError("Must contain at least one special character.")

        return password

    # ---------------- CROSS FIELD VALIDATION ----------------
    def clean(self):
        cleaned_data = super().clean()

        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")

        return cleaned_data

    # ---------------- SAFE SAVE METHOD ----------------
    def save(self, commit=True):
        user = super().save(commit=False)

        # IMPORTANT: hash password ONLY once here
        user.set_password(self.cleaned_data['password'])

        if commit:
            user.save()

            # assign group safely
            role_to_group = {
                'ADMIN': 'Admin',
                'HR': 'HR',
                'MANAGER': 'Manager',
                'EMPLOYEE': 'Employee'
            }

            group_name = role_to_group.get(user.role, 'Employee')

            group, _ = Group.objects.get_or_create(name=group_name)
            user.groups.add(group)

        return user


# ---------------- LOGIN FORM ----------------
class LoginForm(forms.Form):

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
# ---------------- PROFILE UPDATE FORM ----------------

class ProfileUpdateForm(forms.ModelForm):

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'email',
            'phone',
            'profile_image'
        ]

        widgets = {
            'first_name': forms.TextInput(
                attrs={'class': 'form-control'}
            ),
            'last_name': forms.TextInput(
                attrs={'class': 'form-control'}
            ),
            'email': forms.EmailInput(
                attrs={'class': 'form-control'}
            ),
            'phone': forms.TextInput(
                attrs={'class': 'form-control'}
            ),
        }