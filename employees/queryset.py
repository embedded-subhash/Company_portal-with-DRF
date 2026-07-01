from django.db import models
from django.utils import timezone


class EmployeeQuerySet(models.QuerySet):

    def active(self):
        return self.filter(
            status=True
        )

    def high_salary(self):
        return self.filter(
            salary__gte=100000
        )

    def joined_this_month(self):

        today = timezone.now()

        return self.filter(
            joining_date__year=today.year,
            joining_date__month=today.month
        )