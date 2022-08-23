from django.db.models import QuerySet
from rest_framework.request import Request
from rest_framework.pagination import LimitOffsetPagination, _positive_int


class BasicPagination(LimitOffsetPagination):
    default_limit = 10
    max_limit = 25

    def get_limit(self, request: Request) -> int:
        try:
            return _positive_int(
                request.query_params.get('limit'),
                cutoff=self.max_limit
            )
        except (TypeError, ValueError):
            return self.default_limit

    def get_offset(self, request: Request) -> int:
        try:
            return _positive_int(request.query_params.get('offset'))
        except (TypeError, ValueError):
            return 0

    def paginate_queryset(self, queryset: QuerySet, request: Request, view=None):
        limit = self.get_limit(request)
        offset = self.get_offset(request)
        return queryset[offset:offset + limit]
