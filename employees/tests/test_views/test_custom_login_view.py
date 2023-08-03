from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from ...views.CustomLoginView import CustomLoginView


class CustomLoginViewTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.tested_class = CustomLoginView
        cls.url = reverse('login')

        cls.user = User.objects.create_user(**{
            'username': 'q' * 50,
            'email': 'q' * 50 + 'q@q.q',
            'password': 'q' * 50,
        })

    def test_Should_InheritDefiniteClasses(self):
        expected_super_classes = (
            LoginView,
        )
        real_super_classes = self.tested_class.__bases__

        self.assertEqual(expected_super_classes, real_super_classes)

    def test_Should_SetTemplateName(self):
        expected_template_name = 'login.html'
        real_template_name = self.tested_class.template_name

        self.assertEqual(expected_template_name, real_template_name)

    def test_Should_SetNextPage(self):
        expected_next_page = reverse('employee_template')
        real_next_page = self.tested_class.next_page

        self.assertEqual(expected_next_page, real_next_page)

    def test_Should_RedirectAuthenticatedUserAsTrue(self):
        expected_redirect = True
        real_redirect = self.tested_class.redirect_authenticated_user

        self.assertEqual(expected_redirect, real_redirect)

    def test_When_PutMethodOnEmployeeTemplate_Should_ErrorWith405(self):
        response = self.client.put(self.url, {})

        expected_status = status.HTTP_200_OK
        real_status = response.status_code

        expected_message = (
            '<p>Неверный логин или пароль.</p>'
        )
        real_data = response.content.decode('utf-8')

        self.assertEqual(expected_status, real_status)
        self.assertIn(expected_message, real_data)

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

    def test_When_PostMethodOnEmployeeTemplate_Should_DataWith301(self):
        response = self.client.post(self.url, {
            'username': 'q' * 50,
            'password': 'q' * 50,
        })

        expected_status = status.HTTP_302_FOUND
        real_status = response.status_code

        self.assertEqual(expected_status, real_status)

    def test_When_GetMethodOnEmployeeTemplateWithOutAuth_Should_NoAuthWith200(
            self):
        response = self.client.get(self.url)

        expected_status = status.HTTP_200_OK
        real_status = response.status_code

        data = response.content.decode('utf-8').replace('  ', '')

        expected_username_field = '\n'.join([
            '<input type="text" class="form-control"',
            ' name="username" autofocus=""',
            ' autocapitalize="none"',
            ' autocomplete="username" required=""',
            ' id="id_username">',
        ])
        real_username_field = data

        expected_password_field = '\n'.join([
            '<input type="password" class="form-control"',
            ' name="password"',
            ' autocomplete="current-password" required=""',
            ' id="id_password">',
        ])
        real_password_field = data

        self.assertEqual(expected_status, real_status)
        self.assertIn(expected_username_field, real_username_field)
        self.assertIn(expected_username_field, real_username_field)
        self.assertIn(expected_password_field, real_password_field)
