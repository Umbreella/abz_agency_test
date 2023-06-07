from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.test import APITestCase
from rest_framework.viewsets import ModelViewSet

from ...models.JobTitle import JobTitle
from ...serializers.JobTitleSerializer import JobTitleSerializer
from ...views.JobTitleViewSet import JobTitleViewSet


class EmployeeViewSetTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.tested_class = JobTitleViewSet
        cls.queryset = JobTitle.objects.all()
        cls.serializer = JobTitleSerializer
        cls.url = reverse('list_jobtitle')

        user = User.objects.create_user(**{
            'username': 'q' * 50,
            'email': 'q' * 50 + 'q@q.q',
            'password': 'q' * 50,
        })

        cls.job_title = JobTitle.objects.create(**{
            'title': 'q' * 50,
        })

        cls.data = {
            'title': 'q' * 50,
        }

        client = cls.client_class()
        client.force_authenticate(user=user)
        cls.logged_client = client

    def test_Should_InheritModelViewSet(self):
        expected_super_classes = (
            ModelViewSet,
        )
        real_super_classes = self.tested_class.__bases__

        self.assertEqual(expected_super_classes, real_super_classes)

    def test_Should_QuerySetAsAllEmployees(self):
        expected_queryset = str(self.queryset.query)
        real_queryset = str(self.tested_class.queryset.query)

        self.assertEqual(expected_queryset, real_queryset)

    def test_Should_PermissionClassesIsAuthenticated(self):
        expected_permission_classes = (
            IsAuthenticated,
        )
        real_permission_classes = self.tested_class.permission_classes

        self.assertEqual(expected_permission_classes, real_permission_classes)

    def test_Should_SerializerClassIsEmployeeWithBossSerializer(self):
        expected_serializer = self.serializer
        real_serializer = self.tested_class.serializer_class

        self.assertEqual(expected_serializer, real_serializer)

    def test_Should_FilterBackendsAsListOfDefinedFilters(self):
        expected_filter_backends = (
            OrderingFilter,
        )
        real_filter_backends = self.tested_class.filter_backends

        self.assertEqual(expected_filter_backends, real_filter_backends)

    def test_Should_DefaultOrderingAsId(self):
        expected_fields = (
            'id',
        )
        real_fields = self.tested_class.ordering

        self.assertEqual(expected_fields, real_fields)

    def test_Should_DontOverrideSuperMethods(self):
        expected_methods = [
            ModelViewSet.list,
            ModelViewSet.create,
            ModelViewSet.destroy,
            ModelViewSet.retrieve,
            ModelViewSet.update,
            ModelViewSet.partial_update,
        ]
        real_methods = [
            self.tested_class.list,
            self.tested_class.create,
            self.tested_class.destroy,
            self.tested_class.retrieve,
            self.tested_class.update,
            self.tested_class.partial_update,
        ]

        self.assertEqual(expected_methods, real_methods)

    def test_When_PostMethodForListEmployees_Should_ErrorWithStatus405(self):
        response = self.logged_client.post(self.url, {})

        expected_status = status.HTTP_405_METHOD_NOT_ALLOWED
        real_status = response.status_code

        self.assertEqual(expected_status, real_status)

    def test_When_PutMethodForListEmployees_Should_ErrorWithStatus405(self):
        response = self.logged_client.put(self.url)

        expected_status = status.HTTP_405_METHOD_NOT_ALLOWED
        real_status = response.status_code

        self.assertEqual(expected_status, real_status)

    def test_When_PatchMethodForListEmployees_Should_ErrorWithStatus405(self):
        response = self.logged_client.patch(self.url)

        expected_status = status.HTTP_405_METHOD_NOT_ALLOWED
        real_status = response.status_code

        self.assertEqual(expected_status, real_status)

    def test_When_DeleteMethodForListEmployees_Should_ErrorWithStatus405(
            self):
        response = self.logged_client.delete(self.url)

        expected_status = status.HTTP_405_METHOD_NOT_ALLOWED
        real_status = response.status_code

        self.assertEqual(expected_status, real_status)

    def test_When_GetMethodForListEmployees_Should_ReturnDataWithStatus200(
            self):
        response = self.logged_client.get(self.url)

        expected_status = status.HTTP_200_OK
        real_status = response.status_code

        expected_data = {
            'count': 1,
            'next': None,
            'previous': None,
            'results': self.serializer(**{
                'instance': self.queryset,
                'many': True,
            }).data,
        }
        real_data = dict(response.data)

        self.maxDiff = None

        self.assertEqual(expected_status, real_status)
        self.assertEqual(expected_data, real_data)
