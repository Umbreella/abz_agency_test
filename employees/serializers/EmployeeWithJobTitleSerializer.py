from rest_framework.serializers import ImageField, PrimaryKeyRelatedField

from ..models.JobTitle import JobTitle
from .EmployeeSerializer import EmployeeSerializer
from .JobTitleSerializer import JobTitleSerializer


class EmployeeWithJobTitleSerializer(EmployeeSerializer):
    photo = ImageField(required=False)
    job_title = JobTitleSerializer(read_only=True)
    job_title_id = PrimaryKeyRelatedField(source='job_title',
                                          queryset=JobTitle.objects.all(),
                                          write_only=True)

    class Meta:
        model = EmployeeSerializer.Meta.model
        fields = (
            *EmployeeSerializer.Meta.fields,
            'date_of_receipt', 'wage', 'photo', 'job_title', 'job_title_id',
        )
