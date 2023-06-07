from django.test import TestCase
from rest_framework.filters import BaseFilterBackend

from ...filtersets.EmployeeBossFilterBackend import EmployeeBossFilterBackend
from ...models.Employee import Employee
from ...models.JobTitle import JobTitle


class EmployeeBossFilterBackendTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.tested_class = EmployeeBossFilterBackend
        cls.queryset = Employee.objects.all()

        job_title = JobTitle.objects.create(**{
            'title': 'q' * 50,
        })

        boss = Employee.objects.create(**{
            'id': 1,
            'first_name': 'q' * 50,
            'middle_name': 'q' * 50,
            'last_name': 'q' * 50,
            'wage': 1_000,
            'job_title': job_title,
        })

        Employee.objects.create(**{
            'id': 2,
            'first_name': 'q' * 50,
            'middle_name': 'q' * 50,
            'last_name': 'q' * 50,
            'wage': 1_000,
            'job_title': job_title,
            'boss': boss,
        })

        Employee.objects.create(**{
            'id': 3,
            'first_name': 'q' * 50,
            'middle_name': 'q' * 50,
            'last_name': 'q' * 50,
            'wage': 1_000,
            'job_title': job_title,
        })

        Employee.objects.create(**{
            'id': 4,
            'first_name': 'q' * 50,
            'middle_name': 'q' * 50,
            'last_name': 'q' * 50,
            'wage': 1_000,
            'job_title': job_title,
            'boss': boss,
        })

    def setUp(self):
        self.request = type('request', (object,), {
            'query_params': {
                'boss_null': '1',
            },
        })

    def test_Should_InheritDefiniteClasses(self):
        expected_bases = (
            BaseFilterBackend,
        )
        real_bases = self.tested_class.__bases__

        self.assertEqual(expected_bases, real_bases)

    def test_Should_DontOverrideSuperMethods(self):
        expected_methods = (
            BaseFilterBackend.get_schema_fields,
            BaseFilterBackend.get_schema_operation_parameters,
        )
        real_methods = (
            self.tested_class.get_schema_fields,
            self.tested_class.get_schema_operation_parameters,
        )

        self.assertEqual(expected_methods, real_methods)

    def test_Should_OverrideSuperMethods(self):
        expected_methods = (
            BaseFilterBackend.filter_queryset,
        )
        real_methods = (
            self.tested_class.filter_queryset,
        )

        self.assertNotEqual(expected_methods, real_methods)

    def test_When_RequestWithEmptyParams_Should_DontChangeQuerySet(self):
        request = self.request
        request.query_params = {}

        expected_queryset = list(self.queryset)
        real_queryset = list(self.tested_class().filter_queryset(**{
            'request': request,
            'queryset': self.queryset,
            'view': None,
        }))

        self.assertEqual(expected_queryset, real_queryset)

    def test_When_BossNullParamsIsEmpty_Should_DontChangeQuerySet(self):
        request = self.request
        request.query_params = {
            'boss_null': None,
        }

        expected_queryset = list(self.queryset)
        real_queryset = list(self.tested_class().filter_queryset(**{
            'request': request,
            'queryset': self.queryset,
            'view': None,
        }))

        self.assertEqual(expected_queryset, real_queryset)

    def test_When_BossNullParamsIsZero_Should_DontChangeQuerySet(self):
        request = self.request
        request.query_params = {
            'boss_null': '0',
        }

        expected_queryset = list(self.queryset)
        real_queryset = list(self.tested_class().filter_queryset(**{
            'request': request,
            'queryset': self.queryset,
            'view': None,
        }))

        self.assertEqual(expected_queryset, real_queryset)

    def test_When_BossNullParamsIsOne_Should_ChangeQuerySet(self):
        expected_queryset = list(self.queryset.filter(boss__isnull=True))
        real_queryset = list(self.tested_class().filter_queryset(**{
            'request': self.request,
            'queryset': self.queryset,
            'view': None,
        }))

        self.assertEqual(expected_queryset, real_queryset)
