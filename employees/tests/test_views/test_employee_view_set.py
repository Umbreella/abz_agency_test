from datetime import timedelta

from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.test import APITestCase
from rest_framework.viewsets import ModelViewSet

from ...filtersets.EmployeeBossFilterBackend import EmployeeBossFilterBackend
from ...models.Employee import Employee
from ...models.JobTitle import JobTitle
from ...serializers.EmployeeWithBossSerializer import \
    EmployeeWithBossSerializer
from ...views.EmployeeViewSet import EmployeeViewSet


class EmployeeViewSetTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.tested_class = EmployeeViewSet
        cls.queryset = Employee.objects.select_related(
            'job_title', 'boss',
        ).all()
        cls.serializer = EmployeeWithBossSerializer
        cls.list_url = reverse('list_employee')
        cls.single_url = reverse('single_employee', kwargs={'pk': 1, })

        user = User.objects.create_user(**{
            'username': 'q' * 50,
            'email': 'q' * 50 + 'q@q.q',
            'password': 'q' * 50,
        })

        job_title = JobTitle.objects.create(**{
            'title': 'q' * 50,
        })

        cls.employee = Employee.objects.create(**{
            'id': 1,
            'first_name': 'q' * 50,
            'middle_name': 'q' * 50,
            'last_name': 'q' * 50,
            'wage': 1000.0,
            'job_title': job_title,
        })

        Employee.objects.create(**{
            'id': 2,
            'first_name': 'w' * 50,
            'middle_name': 'w' * 50,
            'last_name': 'w' * 50,
            'wage': 1000.0,
            'job_title': job_title,
        })

        cls.data = {
            'first_name': 'q' * 50,
            'middle_name': 'q' * 50,
            'last_name': 'q' * 50,
            'date_of_receipt': (timezone.now() - timedelta(days=1)).date(),
            'wage': 1000.0,
            'job_title_id': job_title.id,
            'boss_id': cls.employee.id,
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
            DjangoFilterBackend, SearchFilter, OrderingFilter,
            EmployeeBossFilterBackend,
        )
        real_filter_backends = self.tested_class.filter_backends

        self.assertEqual(expected_filter_backends, real_filter_backends)

    def test_Should_DefiniteFiltersetFields(self):
        expected_fields = (
            'boss',
        )
        real_fields = self.tested_class.filterset_fields

        self.assertEqual(expected_fields, real_fields)

    def test_Should_DefiniteSearchFields(self):
        expected_fields = (
            'first_name', 'middle_name', 'last_name', 'job_title__title',
            'date_of_receipt', 'wage',
        )
        real_fields = self.tested_class.search_fields

        self.assertEqual(expected_fields, real_fields)

    def test_Should_DefiniteOrderingFields(self):
        expected_fields = (
            'first_name', 'middle_name', 'last_name', 'job_title__title',
            'date_of_receipt', 'wage',
        )
        real_fields = self.tested_class.ordering_fields

        self.assertEqual(expected_fields, real_fields)

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

    def test_When_PutMethodForListEmployees_Should_ErrorWithStatus405(self):
        response = self.logged_client.put(self.list_url)

        expected_status = status.HTTP_405_METHOD_NOT_ALLOWED
        real_status = response.status_code

        self.assertEqual(expected_status, real_status)

    def test_When_PatchMethodForListEmployees_Should_ErrorWithStatus405(self):
        response = self.logged_client.patch(self.list_url)

        expected_status = status.HTTP_405_METHOD_NOT_ALLOWED
        real_status = response.status_code

        self.assertEqual(expected_status, real_status)

    def test_When_DeleteMethodForListEmployees_Should_ErrorWithStatus405(
            self):
        response = self.logged_client.delete(self.list_url)

        expected_status = status.HTTP_405_METHOD_NOT_ALLOWED
        real_status = response.status_code

        self.assertEqual(expected_status, real_status)

    def test_When_GetMethodForListEmployees_Should_ReturnDataWithStatus200(
            self):
        response = self.logged_client.get(self.list_url)

        expected_status = status.HTTP_200_OK
        real_status = response.status_code

        expected_data = {
            'count': 2,
            'next': None,
            'previous': None,
            'results': self.serializer(**{
                'instance': self.queryset.order_by('id'),
                'many': True,
            }).data,
        }
        real_data = dict(response.data)

        self.maxDiff = None

        self.assertEqual(expected_status, real_status)
        self.assertEqual(expected_data, real_data)

    def test_When_PostMethodForListEmployees_Should_ReturnDataWithStatus201(
            self):
        data = self.data
        response = self.logged_client.post(self.list_url, data)

        expected_status = status.HTTP_201_CREATED
        real_status = response.status_code

        expected_data = self.serializer(self.queryset.last()).data
        real_data = response.data

        self.assertEqual(expected_status, real_status)
        self.assertEqual(expected_data, real_data)

    def test_When_PostMethodForSingleEmployee_Should_ReturnDataWithStatus200(
            self):
        response = self.logged_client.post(self.single_url, {})

        expected_status = status.HTTP_405_METHOD_NOT_ALLOWED
        real_status = response.status_code

        self.assertEqual(expected_status, real_status)

    def test_When_GetMethodForSingleEmployee_Should_ReturnDataWithStatus200(
            self):
        response = self.logged_client.get(self.single_url)

        expected_status = status.HTTP_200_OK
        real_status = response.status_code

        expected_data = self.serializer(self.employee).data
        real_data = response.data

        self.assertEqual(expected_status, real_status)
        self.assertEqual(expected_data, real_data)

    def test_When_PutMethodForSingleEmployee_Should_ReturnDataWithStatus200(
            self):
        data = self.data
        response = self.logged_client.put(self.single_url, data)
        self.employee.refresh_from_db()

        expected_status = status.HTTP_200_OK
        real_status = response.status_code

        expected_data = self.serializer(self.employee).data
        real_data = response.data

        self.assertEqual(expected_status, real_status)
        self.assertEqual(expected_data, real_data)

    def test_When_PatchMethodForSingleEmployee_Should_ReturnDataWithStatus200(
            self):
        data = self.data

        response = self.logged_client.patch(self.single_url, data)
        self.employee.refresh_from_db()

        expected_status = status.HTTP_200_OK
        real_status = response.status_code

        expected_data = self.serializer(self.employee).data
        real_data = response.data

        self.assertEqual(expected_status, real_status)
        self.assertEqual(expected_data, real_data)

    def test_When_DeleteMethodForSingleEmployee_Should_ReturnDataWithStatus200(
            self):
        response = self.logged_client.delete(self.single_url)

        expected_status = status.HTTP_204_NO_CONTENT
        real_status = response.status_code

        self.assertEqual(expected_status, real_status)
