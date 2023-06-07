from django.core.exceptions import ValidationError
from django.db.models import (BigAutoField, CharField, DateField, DecimalField,
                              ForeignKey, ImageField, ManyToOneRel)
from django.test import TestCase
from django.utils import timezone

from ...models.Employee import Employee
from ...models.JobTitle import JobTitle


class JobTitleTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.tested_class = Employee

        job_title = JobTitle.objects.create(**{
            'title': 'q' * 50,
        })

        boss = Employee.objects.create(**{
            'first_name': 'q' * 50,
            'middle_name': 'q' * 50,
            'last_name': 'q' * 50,
            'wage': 1000.0,
            'job_title': job_title,
        })

        cls.data = {
            'first_name': 'q' * 50,
            'middle_name': 'q' * 50,
            'last_name': 'q' * 50,
            'wage': 100.0,
            'job_title': job_title,
            'boss': boss,
        }

    def test_Should_IncludeRequiredFields(self):
        expected_fields = [
            'employee', 'id', 'first_name', 'middle_name', 'last_name',
            'date_of_receipt', 'wage', 'job_title', 'boss', 'photo',
        ]
        real_fields = [
            field.name for field in self.tested_class._meta.get_fields()
        ]

        self.assertEqual(expected_fields, real_fields)

    def test_Should_SpecificTypeForEachField(self):
        expected_fields = {
            'id': BigAutoField,
            'first_name': CharField,
            'middle_name': CharField,
            'last_name': CharField,
            'date_of_receipt': DateField,
            'wage': DecimalField,
            'job_title': ForeignKey,
            'boss': ForeignKey,
            'photo': ImageField,
            'employee': ManyToOneRel,
        }
        real_fields = {
            field.name: field.__class__
            for field in self.tested_class._meta.get_fields()
        }
        self.maxDiff = None

        self.assertEqual(expected_fields, real_fields)

    def test_Should_HelpTextForEachField(self):
        expected_help_text = {
            'id': '',
            'first_name': 'Employee first name',
            'middle_name': 'Employee middle name',
            'last_name': 'Employee last name',
            'date_of_receipt': 'Employee date of receipt on job',
            'wage': 'Employee wage for work',
            'job_title': 'Employee job title',
            'boss': 'Employee boss',
            'photo': 'Employee photo',
            'employee': '',

        }
        real_help_text = {
            field.name: (
                field.help_text if hasattr(field, 'help_text') else ''
            )
            for field in self.tested_class._meta.get_fields()
        }

        self.assertEqual(expected_help_text, real_help_text)

    def test_When_DataIsEmpty_Should_ErrorBlankFields(self):
        employee = self.tested_class()

        with self.assertRaises(ValidationError) as _raise:
            employee.save()

        expected_raise = {
            'first_name': [
                'This field cannot be blank.',
            ],
            'middle_name': [
                'This field cannot be blank.',
            ],
            'last_name': [
                'This field cannot be blank.',
            ],
            'job_title': [
                'This field cannot be null.',
            ],
            'wage': [
                'This field cannot be null.',
            ],
        }
        real_raise = _raise.exception.message_dict

        self.assertEqual(expected_raise, real_raise)

    def test_When_LengthDataGreaterThanMaxLength_Should_ErrorMaxLength(self):
        data = self.data
        data.update({
            'first_name': 'q' * 275,
            'middle_name': 'q' * 275,
            'last_name': 'q' * 275,
        })

        employee = self.tested_class(**data)

        with self.assertRaises(ValidationError) as _raise:
            employee.save()

        expected_raise = {
            'first_name': [
                'Ensure this value has at most 255 characters (it has 275).',
            ],
            'middle_name': [
                'Ensure this value has at most 255 characters (it has 275).',
            ],
            'last_name': [
                'Ensure this value has at most 255 characters (it has 275).',
            ],
        }
        real_raise = _raise.exception.message_dict

        self.assertEqual(expected_raise, real_raise)

    def test_When_DataIsValid_Should_CreateJobTitle(self):
        data = self.data

        employee = self.tested_class(**data)
        employee.save()

        expected_date_of_receipt = timezone.now().date()
        real_date_of_receipt = employee.date_of_receipt

        self.assertEqual(expected_date_of_receipt, real_date_of_receipt)
