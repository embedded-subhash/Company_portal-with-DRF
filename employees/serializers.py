from datetime import date
from rest_framework import serializers


def validate_joining_date(self, value):

    if value > date.today():
        raise serializers.ValidationError(
            "Joining date cannot be in the future."
        )

    return value