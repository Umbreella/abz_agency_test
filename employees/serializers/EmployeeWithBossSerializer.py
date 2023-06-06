from rest_framework.serializers import PrimaryKeyRelatedField

from ..models.Employee import Employee
from .EmployeeSerializer import EmployeeSerializer
from .EmployeeWithJobTitleSerializer import EmployeeWithJobTitleSerializer


class EmployeeWithBossSerializer(EmployeeWithJobTitleSerializer):
    boss = EmployeeSerializer(read_only=True)
    boss_id = PrimaryKeyRelatedField(source='boss',
                                     queryset=Employee.objects.all(),
                                     write_only=True, allow_null=True)

    class Meta:
        model = EmployeeWithJobTitleSerializer.Meta.model
        fields = (
            *EmployeeWithJobTitleSerializer.Meta.fields,
            'boss', 'boss_id',
        )
