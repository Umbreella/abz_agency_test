from rest_framework.serializers import ModelSerializer

from ..models.JobTitle import JobTitle


class JobTitleSerializer(ModelSerializer):
    class Meta:
        model = JobTitle
        fields = (
            'id', 'title',
        )
