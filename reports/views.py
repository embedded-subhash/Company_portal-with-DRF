from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from api.pagination import AuditLogPagination
from api.permissions import IsAdmin
from api.responses import SuccessResponse

from .models import AuditLog
from .serializers import AuditLogSerializer


class AuditLogViewSet(viewsets.ReadOnlyModelViewSet):
    """Read-only audit trail. 50 records per page. Admin only."""

    queryset = AuditLog.objects.select_related("user").all()
    serializer_class = AuditLogSerializer
    pagination_class = AuditLogPagination
    permission_classes = [IsAuthenticated, IsAdmin]
    ordering_fields = ["created_at"]
    search_fields = ["action", "details"]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page if page is not None else queryset, many=True)
        if page is not None:
            paginated = self.get_paginated_response(serializer.data)
            return SuccessResponse(message="Audit Logs Fetched Successfully", data=paginated.data)
        return SuccessResponse(message="Audit Logs Fetched Successfully", data=serializer.data)
