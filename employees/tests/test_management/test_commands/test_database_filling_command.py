from django.core.management import BaseCommand
from django.test import TestCase

from ....management.commands.database_filling import Command
from ....models.Employee import Employee
from ....models.JobTitle import JobTitle


class DataBaseFillingCommandTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.tested_class = Command

    def test_Should_InheritDefiniteClasses(self):
        expected_bases = (
            BaseCommand,
        )
        real_bases = self.tested_class.__bases__

        self.assertEqual(expected_bases, real_bases)

    def test_Should_OverrideSuperMethods(self):
        expected_methods = (
            BaseCommand.handle,
        )
        real_methods = (
            self.tested_class.handle,
        )

        self.assertNotEqual(expected_methods, real_methods)

    def test_When_CallMethodHandle_Should_FillingDatabase(self):
        self.tested_class().handle()

        expected_count_job_title = 100
        real_count_job_title = JobTitle.objects.count()

        expected_count_employee = 50_000
        real_count_employee = Employee.objects.count()

        self.assertEqual(expected_count_job_title, real_count_job_title)
        self.assertEqual(expected_count_employee, real_count_employee)
