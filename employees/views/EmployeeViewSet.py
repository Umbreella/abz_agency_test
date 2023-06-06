from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from ..filtersets.EmployeeBossFilterBackend import EmployeeBossFilterBackend
from ..models.Employee import Employee
from ..serializers.EmployeeWithBossSerializer import EmployeeWithBossSerializer


class EmployeeViewSet(ModelViewSet):
    queryset = Employee.objects.select_related(
        'job_title', 'boss',
    ).all()
    permission_classes = (IsAuthenticated,)
    serializer_class = EmployeeWithBossSerializer
    filter_backends = (
        DjangoFilterBackend, SearchFilter, OrderingFilter,
        EmployeeBossFilterBackend,
    )
    filterset_fields = ('boss',)
    search_fields = (
        'first_name', 'middle_name', 'last_name', 'job_title__title',
        'date_of_receipt', 'wage',
    )
    ordering_fields = (
        'first_name', 'middle_name', 'last_name', 'job_title__title',
        'date_of_receipt', 'wage',
    )
    ordering = ('id',)
