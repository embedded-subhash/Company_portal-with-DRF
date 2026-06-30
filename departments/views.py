from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    ListView,
    UpdateView,
    DeleteView,
    DetailView
)

from .models import Department


class DepartmentCreateView(CreateView):
    model = Department
    fields = '__all__'
    template_name = 'departments/create.html'
    success_url = reverse_lazy('department_list')


class DepartmentListView(ListView):
    model = Department
    template_name = 'departments/list.html'
    context_object_name = 'departments'


class DepartmentDetailView(DetailView):
    model = Department
    template_name = 'departments/detail.html'
    context_object_name = 'department'


class DepartmentUpdateView(UpdateView):
    model = Department
    fields = '__all__'
    template_name = 'departments/update.html'
    success_url = reverse_lazy('department_list')


class DepartmentDeleteView(DeleteView):
    model = Department
    template_name = 'departments/delete.html'
    success_url = reverse_lazy('department_list')