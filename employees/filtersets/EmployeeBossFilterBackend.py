from rest_framework.filters import BaseFilterBackend


class EmployeeBossFilterBackend(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        boss_is_null = request.query_params.get('boss_null')

        if boss_is_null and boss_is_null == '1':
            queryset = queryset.filter(boss__isnull=True)

        return queryset
