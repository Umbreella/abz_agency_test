from django.core.exceptions import ValidationError
from django.db.models import BigAutoField, CharField, ManyToOneRel
from django.test import TestCase

from ...models.JobTitle import JobTitle


class JobTitleTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.tested_class = JobTitle

        cls.data = {
            'title': 'q' * 50,
        }

    def test_Should_IncludeRequiredFields(self):
        expected_fields = [
            'employee', 'id', 'title',
        ]
        real_fields = [
            field.name for field in self.tested_class._meta.get_fields()
        ]

        self.assertEqual(expected_fields, real_fields)

    def test_Should_SpecificTypeForEachField(self):
        expected_fields = {
            'id': BigAutoField,
            'title': CharField,
            'employee': ManyToOneRel,
        }
        real_fields = {
            field.name: field.__class__
            for field in self.tested_class._meta.get_fields()
        }

        self.assertEqual(expected_fields, real_fields)

    def test_Should_HelpTextForEachField(self):
        expected_help_text = {
            'id': '',
            'title': 'Job title.',
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
        job_title = self.tested_class()

        with self.assertRaises(ValidationError) as _raise:
            job_title.save()

        expected_raise = {
            'title': [
                'This field cannot be blank.',
            ],
        }
        real_raise = _raise.exception.message_dict

        self.assertEqual(expected_raise, real_raise)

    def test_When_LengthDataGreaterThanMaxLength_Should_ErrorMaxLength(self):
        data = self.data
        data.update({
            'title': 'q' * 275,
        })

        job_title = self.tested_class(**data)

        with self.assertRaises(ValidationError) as _raise:
            job_title.save()

        expected_raise = {
            'title': [
                'Ensure this value has at most 255 characters (it has 275).',
            ],
        }
        real_raise = _raise.exception.message_dict

        self.assertEqual(expected_raise, real_raise)

    def test_When_DataIsValid_Should_CreateJobTitle(self):
        data = self.data

        job_title = self.tested_class(**data)
        job_title.save()

        expected_str = job_title.title
        real_str = str(job_title)

        self.assertEqual(expected_str, real_str)
