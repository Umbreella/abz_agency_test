from django.contrib.auth.models import User
from django.urls import reverse
from django.views.generic import TemplateView
from rest_framework import status
from rest_framework.test import APITestCase

from ...views.EmployeeTemplateView import EmployeeTemplateView


class EmployeeTemplateViewTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.tested_class = EmployeeTemplateView
        cls.url = reverse('employee_template')

        cls.user = User.objects.create_user(**{
            'username': 'q' * 50,
            'email': 'q' * 50 + 'q@q.q',
            'password': 'q' * 50,
        })

    def test_Should_InheritDefiniteClasses(self):
        expected_super_classes = (
            TemplateView,
        )
        real_super_classes = self.tested_class.__bases__

        self.assertEqual(expected_super_classes, real_super_classes)

    def test_Should_OverrideSuperMethods(self):
        expected_methods = (
            TemplateView.get_context_data,
        )
        real_methods = (
            self.tested_class.get_context_data,
        )

        self.assertNotEqual(expected_methods, real_methods)

    def test_Should_SetTemplateName(self):
        expected_template_name = 'employee_table.html'
        real_template_name = self.tested_class.template_name

        self.assertEqual(expected_template_name, real_template_name)

    def test_When_CallGetContextData_Should_AddUserInContext(self):
        request = type('request', (object,), {
            'user': self.user,
        })

        employee_template_view = self.tested_class()
        employee_template_view.setup(request)

        context = employee_template_view.get_context_data()

        expected_keys = [
            'view', 'user',
        ]
        real_keys = list(context.keys())

        expected_value = self.user
        real_value = context.get('user')

        self.assertEqual(expected_keys, real_keys)
        self.assertEqual(expected_value, real_value)

    def test_When_PostMethodOnEmployeeTemplate_Should_ErrorWith405(self):
        response = self.client.post(self.url, {})

        expected_status = status.HTTP_405_METHOD_NOT_ALLOWED
        real_status = response.status_code

        self.assertEqual(expected_status, real_status)

    def test_When_PutMethodOnEmployeeTemplate_Should_ErrorWith405(self):
        response = self.client.put(self.url, {})

        expected_status = status.HTTP_405_METHOD_NOT_ALLOWED
        real_status = response.status_code

        self.assertEqual(expected_status, real_status)

    def test_When_PatchMethodOnEmployeeTemplate_Should_ErrorWith405(self):
        response = self.client.patch(self.url, {})

        expected_status = status.HTTP_405_METHOD_NOT_ALLOWED
        real_status = response.status_code

        self.assertEqual(expected_status, real_status)

    def test_When_DeleteMethodOnEmployeeTemplate_Should_ErrorWith405(self):
        response = self.client.delete(self.url)

        expected_status = status.HTTP_405_METHOD_NOT_ALLOWED
        real_status = response.status_code

        self.assertEqual(expected_status, real_status)

    def test_When_GetMethodOnEmployeeTemplateWithOutAuth_Should_NoAuthWith200(
            self):
        response = self.client.get(self.url)

        expected_status = status.HTTP_200_OK
        real_status = response.status_code

        expected_data = '\n'.join([
            '<h5 class="card-title">Вы не авторизованы</h5>',
            '<p class="card-text">',
            'Для доступа к данной странице, необходимо быть авторизованным.',
            '</p>',
        ])
        real_data = response.content.decode('utf-8').replace('  ', '')

        self.assertEqual(expected_status, real_status)
        self.assertIn(expected_data, real_data)

    def test_When_GetMethodOnEmployeeTemplateWithAuth_Should_DataWith200(
            self):
        client = self.client
        client.force_login(self.user)

        response = client.get(self.url)

        expected_status = status.HTTP_200_OK
        real_status = response.status_code

        expected_data = '\n'.join([
            '<h5 class="card-title">Вы не авторизованы</h5>',
            '<p class="card-text">',
            'Для доступа к данной странице, необходимо быть авторизованным.',
            '</p>',
        ])
        real_data = response.content.decode('utf-8').replace('  ', '')

        self.assertEqual(expected_status, real_status)
        self.assertNotIn(expected_data, real_data)
