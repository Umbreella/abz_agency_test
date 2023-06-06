from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from ..models.JobTitle import JobTitle
from ..serializers.JobTitleSerializer import JobTitleSerializer


class JobTitleViewSet(ModelViewSet):
    queryset = JobTitle.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = JobTitleSerializer
    filter_backends = (OrderingFilter,)
    ordering = ('id',)
