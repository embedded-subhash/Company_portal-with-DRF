from rest_framework import generics
from accounts.permissions import IsAdmin
from .models import SecurityLog
from .serializers import SecurityLogSerializer


class SecurityLogListView(generics.ListAPIView):
    """
    Admin-only endpoint to review the security audit trail.
    Supports ?action=LOGIN_FAILURE&status=FAILURE style filtering.
    """
    serializer_class = SecurityLogSerializer
    permission_classes = [IsAdmin]
    queryset = SecurityLog.objects.select_related("user").all()

    def get_queryset(self):
        qs = super().get_queryset()
        action = self.request.query_params.get("action")
        status_param = self.request.query_params.get("status")
        user_id = self.request.query_params.get("user")
        if action:
            qs = qs.filter(action=action)
        if status_param:
            qs = qs.filter(status=status_param)
        if user_id:
            qs = qs.filter(user_id=user_id)
        return qs
