from rest_framework.serializers import ModelSerializer
from snapshottest.django import TestCase

from ...serializers.EmployeeSerializer import EmployeeSerializer
from ...serializers.EmployeeWithJobTitleSerializer import \
    EmployeeWithJobTitleSerializer


class EmployeeWithJobTitleSerializerTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.tested_class = EmployeeWithJobTitleSerializer

    def test_Should_InheritModelSerializer(self):
        expected_super_classes = (
            EmployeeSerializer,
        )
        real_super_classes = self.tested_class.__bases__

        self.assertEqual(expected_super_classes, real_super_classes)

    def test_Should_IncludeDefiniteFieldsFromUserModel(self):
        expected_fields = [
            *EmployeeSerializer.Meta.fields,
            'date_of_receipt', 'wage', 'photo', 'job_title', 'job_title_id',
        ]
        real_fields = list(self.tested_class().get_fields())

        self.assertEqual(expected_fields, real_fields)

    def test_Should_SpecificFormatForEachField(self):
        real_repr = repr(self.tested_class())

        self.assertMatchSnapshot(real_repr)

    def test_Should_DontOverrideSuperMethods(self):
        expected_methods = [
            ModelSerializer.save,
            ModelSerializer.create,
            ModelSerializer.update,
        ]
        real_methods = [
            self.tested_class.save,
            self.tested_class.create,
            self.tested_class.update,
        ]

        self.assertEqual(expected_methods, real_methods)
