"""
Custom pagination classes.

Response shape:
    {
        "count": 2500,
        "next": "...",
        "previous": "...",
        "page": 3,
        "page_size": 20,
        "results": []
    }
"""

from collections import OrderedDict

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class BasePagination(PageNumberPagination):
    """Shared response formatting for all paginators in this project."""

    page_size_query_param = "page_size"
    max_page_size = 200

    def get_paginated_response(self, data):
        return Response(
            OrderedDict(
                [
                    ("count", self.page.paginator.count),
                    ("next", self.get_next_link()),
                    ("previous", self.get_previous_link()),
                    ("page", self.page.number),
                    ("page_size", self.get_page_size(self.request)),
                    ("results", data),
                ]
            )
        )


class StandardResultsPagination(BasePagination):
    """Default pagination (used unless a view overrides it). 20 per page."""

    page_size = 20


class EmployeeListPagination(BasePagination):
    """Employee List -> 20 records per page."""

    page_size = 20


class DepartmentListPagination(BasePagination):
    """Department List -> 10 records per page."""

    page_size = 10


class AuditLogPagination(BasePagination):
    """Audit Logs -> 50 records per page."""

    page_size = 50
