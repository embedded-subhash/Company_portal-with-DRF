from rest_framework import serializers
from .models import SecurityLog


class SecurityLogSerializer(serializers.ModelSerializer):
    user_display = serializers.SerializerMethodField()

    class Meta:
        model = SecurityLog
        fields = [
            "id", "user", "user_display", "actor_identifier", "ip_address",
            "user_agent", "action", "status", "path", "detail", "timestamp",
        ]
        read_only_fields = fields

    def get_user_display(self, obj):
        return obj.actor_identifier or (str(obj.user) if obj.user else "anonymous")
