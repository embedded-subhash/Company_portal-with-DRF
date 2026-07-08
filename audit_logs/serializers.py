from rest_framework import serializers

from .models import AuditLog


class AuditLogSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = AuditLog
        fields = ["id", "user", "action", "module", "timestamp", "ip_address"]
        read_only_fields = fields

    def get_user(self, obj):
        if not obj.user_id:
            return None

        return {
            "id": obj.user.id,
            "email": obj.user.email,
            "role": getattr(obj.user, "role", None),
        }
