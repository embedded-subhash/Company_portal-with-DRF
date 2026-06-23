from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from .forms import UserRegistrationForm, LoginForm
from .decorators import admin_required, hr_required, manager_required
from accounts.models import User
from employees.models import Employee
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from departments.models import Department
from .forms import ProfileUpdateForm
def register(request):

    if request.method == 'POST':

        form = UserRegistrationForm(request.POST)

        if form.is_valid():

            form.save()

            messages.success(
                request,
                'Registration Successful.'
            )

            return redirect('login')

    else:

        form = UserRegistrationForm()

    return render(
        request,
        'accounts/register.html',
        {'form': form}
    )


def login_view(request):

    if request.method == 'POST':

        form = LoginForm(request.POST)

        if form.is_valid():

            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            user = authenticate(
                request,
                username=email,
                password=password
            )

            if user is not None:

                login(request, user)

                if user.role == 'ADMIN':
                    return redirect('admin_dashboard')

                elif user.role == 'HR':
                    return redirect('hr_dashboard')

                elif user.role == 'MANAGER':
                    return redirect('manager_dashboard')

                else:
                    return redirect('employee_dashboard')

            else:

                messages.error(
                    request,
                    'Invalid Email or Password'
                )

    else:

        form = LoginForm()

    return render(
        request,
        'accounts/login.html',
        {'form': form}
    )


@login_required
def dashboard(request):

    return render(
        request,
        'accounts/dashboard.html'
    )


@login_required
 

@login_required
 


@login_required
def logout_view(request):

    logout(request)

    messages.success(
        request,
        'Logged Out Successfully'
    )

    return redirect('login')

@login_required
@admin_required
def admin_dashboard(request):

    context = {
        'total_users': User.objects.count(),
        'active_users': User.objects.filter(
            is_active=True
        ).count(),
        'inactive_users': User.objects.filter(
            is_active=False
        ).count(),
        'total_employees': Employee.objects.count(),
        'total_departments': Department.objects.count(),
        'hr_count': User.objects.filter(
            role='HR'
        ).count(),
        'manager_count': User.objects.filter(
            role='MANAGER'
        ).count(),
        'employee_count': User.objects.filter(
            role='EMPLOYEE'
        ).count(),
    }

    return render(
        request,
        'accounts/admin_dashboard.html',
        context
    )

@login_required
@hr_required
@login_required
@hr_required
def hr_dashboard(request):

    context = {
        'total_employees': Employee.objects.count(),

        'active_employees': Employee.objects.filter(
            status=True
        ).count(),

        'inactive_employees': Employee.objects.filter(
            status=False
        ).count(),

        'total_departments': Department.objects.count(),

        'recent_employees': Employee.objects.order_by(
            '-id'
        )[:5]
    }

    return render(
        request,
        'accounts/hr_dashboard.html',
        context
    )
@login_required
@manager_required
@login_required
@manager_required
def manager_dashboard(request):

    context = {
        'total_employees': Employee.objects.count(),

        'active_employees': Employee.objects.filter(
            status=True
        ).count(),

        'total_departments': Department.objects.count(),
    }

    return render(
        request,
        'accounts/manager_dashboard.html',
        context
    )

@login_required
def employee_dashboard(request):

    return render(
        request,
        'accounts/employee_dashboard.html',
        {
            'user': request.user
        }
    )

@login_required
def change_password(request):

    if request.method == 'POST':

        form = PasswordChangeForm(
            request.user,
            request.POST
        )

        if form.is_valid():

            user = form.save()

            update_session_auth_hash(
                request,
                user
            )

            messages.success(
                request,
                'Password changed successfully.'
            )

            return redirect('dashboard')

    else:

        form = PasswordChangeForm(
            request.user
        )

    return render(
        request,
        'accounts/change_password.html',
        {
            'form': form
        }
    )
@login_required
def profile(request):

    return render(
        request,
        'accounts/profile.html'
    )


@login_required
def edit_profile(request):

    if request.method == 'POST':

        form = ProfileUpdateForm(
            request.POST,
            request.FILES,
            instance=request.user
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                'Profile updated successfully.'
            )

            return redirect('profile')

    else:

        form = ProfileUpdateForm(
            instance=request.user
        )

    return render(
        request,
        'accounts/edit_profile.html',
        {
            'form': form
        }
    )
@login_required
def profile(request):

    return render(
        request,
        'accounts/profile.html'
    )


@login_required
def edit_profile(request):

    if request.method == 'POST':

        form = ProfileUpdateForm(
            request.POST,
            request.FILES,
            instance=request.user
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                'Profile Updated Successfully'
            )

            return redirect('profile')

    else:

        form = ProfileUpdateForm(
            instance=request.user
        )

    return render(
        request,
        'accounts/edit_profile.html',
        {
            'form': form
        }
    )