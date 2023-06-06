from rest_framework.serializers import ModelSerializer

from ..models.Employee import Employee


class EmployeeSerializer(ModelSerializer):
    class Meta:
        model = Employee
        fields = (
            'id', 'first_name', 'middle_name', 'last_name',
        )
