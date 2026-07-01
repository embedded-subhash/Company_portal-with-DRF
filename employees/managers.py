from django.db import models
from .queryset import EmployeeQuerySet  

class ActiveEmployeeManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(
            status=True
        )


class HighSalaryManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(
            salary__gte=100000
        )