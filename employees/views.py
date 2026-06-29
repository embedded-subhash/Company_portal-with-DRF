from django.contrib import messages
from django.urls import reverse_lazy
from django.db.models import Q
from django.shortcuts import redirect

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    CreateView,
    ListView,
    DetailView,
    UpdateView,
    DeleteView
)

from .models import Employee
from .forms import EmployeeForm


class EmployeePermissionMixin(LoginRequiredMixin):

    required_permission = None

    def dispatch(self, request, *args, **kwargs):

        if getattr(request.user, "role", None) == 'ADMIN':
            return super().dispatch(request, *args, **kwargs)

        if self.required_permission:

            if not request.user.has_perm(
                self.required_permission
            ):
                messages.error(
                    request,
                    "You do not have permission."
                )
                return redirect('dashboard')

        return super().dispatch(
            request,
            *args,
            **kwargs
        )


class EmployeeCreateView(
    EmployeePermissionMixin,
    CreateView
):

    required_permission = 'employees.add_employee'

    model = Employee
    form_class = EmployeeForm
    template_name = 'employees/create.html'
    success_url = reverse_lazy('employee_list')

    def form_valid(self, form):

        messages.success(
            self.request,
            'Employee Created Successfully'
        )

        return super().form_valid(form)


class EmployeeListView(
    EmployeePermissionMixin,
    ListView
):

    required_permission = 'employees.view_employee'

    model = Employee
    template_name = 'employees/list.html'
    context_object_name = 'employees'
    paginate_by = 10

    def get_queryset(self):

        queryset = Employee.objects.all()

        search = self.request.GET.get('search')
        department = self.request.GET.get('department')
        status = self.request.GET.get('status')

        if search:
            queryset = queryset.filter(
                Q(employee_id__icontains=search) |
                Q(first_name__icontains=search) |
                Q(last_name__icontains=search) |
                Q(email__icontains=search)
            )

        if department:
            queryset = queryset.filter(
                department__name=department
            )

        if status:
            queryset = queryset.filter(
                status=status
            )

        return queryset

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        from departments.models import Department

        context['departments'] = Department.objects.all()

        return context


class EmployeeDetailView(
    EmployeePermissionMixin,
    DetailView
):

    required_permission = 'employees.view_employee'

    model = Employee
    template_name = 'employees/detail.html'
    context_object_name = 'employee'


class EmployeeUpdateView(
    EmployeePermissionMixin,
    UpdateView
):

    required_permission = 'employees.change_employee'

    model = Employee
    form_class = EmployeeForm
    template_name = 'employees/update.html'
    success_url = reverse_lazy('employee_list')

    def form_valid(self, form):

        messages.success(
            self.request,
            'Employee Updated Successfully'
        )

        return super().form_valid(form)


class EmployeeDeleteView(
    EmployeePermissionMixin,
    DeleteView
):

    required_permission = 'employees.delete_employee'

    model = Employee
    template_name = 'employees/delete.html'
    success_url = reverse_lazy('employee_list')

    def delete(self, request, *args, **kwargs):

        messages.success(
            request,
            'Employee Deleted Successfully'
        )

        return super().delete(
            request,
            *args,
            **kwargs
        )
