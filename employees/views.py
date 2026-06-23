from django.contrib import messages
from django.urls import reverse_lazy
from django.db.models import Q

from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin
)

from django.views.generic import (
    CreateView,
    ListView,
    DetailView,
    UpdateView,
    DeleteView
)

from .models import Employee
from .forms import EmployeeForm


class EmployeeCreateView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    CreateView
):

    permission_required = 'employees.add_employee'

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
    LoginRequiredMixin,
    PermissionRequiredMixin,
    ListView
):

    permission_required = 'employees.view_employee'

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
    LoginRequiredMixin,
    PermissionRequiredMixin,
    DetailView
):

    permission_required = 'employees.view_employee'

    model = Employee
    template_name = 'employees/detail.html'
    context_object_name = 'employee'


class EmployeeUpdateView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    UpdateView
):

    permission_required = 'employees.change_employee'

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
    LoginRequiredMixin,
    PermissionRequiredMixin,
    DeleteView
):

    permission_required = 'employees.delete_employee'

    model = Employee
    template_name = 'employees/delete.html'
    success_url = reverse_lazy('employee_list')

    def form_valid(self, form):

        messages.success(
            self.request,
            'Employee Deleted Successfully'
        )

        return super().form_valid(form)