from django.db import models
from .queryset import EmployeeQuerySet


class EmployeeManager(models.Manager):

    def get_queryset(self):
        return EmployeeQuerySet(
            self.model,
            using=self._db
        )

    def active(self):
        return self.get_queryset().active()

    def high_salary(self):
        return self.get_queryset().high_salary()

    def joined_this_month(self):
        return self.get_queryset().joined_this_month()