from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ReadOnlyModelViewSet

from api.permissions import IsAdminOnly
from api.responses import SuccessResponse
from .models import AuditLog
from .serializers import AuditLogSerializer


class AuditLogViewSet(ReadOnlyModelViewSet):
    queryset = AuditLog.objects.select_related("user").all()
    serializer_class = AuditLogSerializer
    permission_classes = [IsAuthenticated, IsAdminOnly]
    filterset_fields = ["action", "module", "user"]
    search_fields = ["action", "module", "ip_address", "user__email"]
    ordering_fields = ["timestamp", "action", "module"]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            self.paginator.message = "Audit Logs Fetched Successfully"
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return SuccessResponse("Audit Logs Fetched Successfully", serializer.data)

    def retrieve(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_object())
        return SuccessResponse("Audit Log Fetched Successfully", serializer.data)
