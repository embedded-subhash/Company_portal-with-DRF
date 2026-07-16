import factory

from employees.models import Employee
from departments.models import Department


class DepartmentFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Department

    name = factory.Sequence(
        lambda n: f"Department {n}"
    )


class EmployeeFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Employee

    employee_id = factory.Sequence(
        lambda n: f"EMP{100+n}"
    )

    first_name = "John"

    last_name = "Doe"

    email = factory.Sequence(
        lambda n: f"john{n}@company.com"
    )

    designation = "Developer"

    salary = 50000

    department = factory.SubFactory(
        DepartmentFactory
    )