from django.db import models
from datetime import date


class EmployeeQuerySet(models.QuerySet):

    def active(self):
        return self.filter(status=True)

    def inactive(self):
        return self.filter(status=False)

    def high_salary(self):
        return self.filter(salary__gte=50000)

    def joined_this_month(self):
        today = date.today()
        return self.filter(
            joining_date__year=today.year,
            joining_date__month=today.month
        )