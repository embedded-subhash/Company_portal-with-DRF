from django.shortcuts import redirect
from django.contrib import messages


def admin_required(view_func):

    def wrapper(request, *args, **kwargs):

        if request.user.is_authenticated and request.user.role == 'ADMIN':
            return view_func(request, *args, **kwargs)

        messages.error(
            request,
            "Access Denied. Admin Only."
        )

        return redirect('dashboard')

    return wrapper


def hr_required(view_func):

    def wrapper(request, *args, **kwargs):

        if request.user.is_authenticated and request.user.role == 'HR':
            return view_func(request, *args, **kwargs)

        messages.error(
            request,
            "Access Denied. HR Only."
        )

        return redirect('dashboard')

    return wrapper


def manager_required(view_func):

    def wrapper(request, *args, **kwargs):

        if request.user.is_authenticated and request.user.role == 'MANAGER':
            return view_func(request, *args, **kwargs)

        messages.error(
            request,
            "Access Denied. Manager Only."
        )

        return redirect('dashboard')

    return wrapper