from django.contrib.auth.models import User
from django.urls import reverse
from django.views.generic import TemplateView
from rest_framework import status
from rest_framework.test import APITestCase

from ...models.Employee import Employee
from ...models.JobTitle import JobTitle
from ...views.SingleEmployeeTemplateView import SingleEmployeeTemplateView


class SingleEmployeeTemplateViewTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.tested_class = SingleEmployeeTemplateView
        cls.edit_url = reverse('edit_employee_template', kwargs={'pk': 1, })
        cls.create_url = reverse('create_employee_template')

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
        expected_template_name = 'single_employee.html'
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
            'view', 'user', 'operation', 'employee',
        ]
        real_keys = list(context.keys())

        expected_user = self.user
        real_user = context.get('user')

        expected_operation = 'create'
        real_operation = context.get('operation')

        expected_employee = None
        real_employee = context.get('employee')

        self.assertEqual(expected_keys, real_keys)
        self.assertEqual(expected_user, real_user)
        self.assertEqual(expected_operation, real_operation)
        self.assertEqual(expected_employee, real_employee)

    def test_When_CallGetContextDataWithPkInKwargs_Should_OperationIsEdit(
            self):
        job_title = JobTitle.objects.create(**{
            'title': 'q' * 50,
        })

        employee = Employee.objects.create(**{
            'id': 1,
            'first_name': 'q' * 50,
            'middle_name': 'q' * 50,
            'last_name': 'q' * 50,
            'wage': 100.0,
            'job_title': job_title,
        })

        request = type('request', (object,), {
            'user': self.user,
        })

        employee_template_view = self.tested_class()
        employee_template_view.setup(request)

        context = employee_template_view.get_context_data(**{
            'pk': 1,
        })

        expected_value = 'edit'
        real_value = context.get('operation')

        expected_employee = employee
        real_employee = context.get('employee')

        self.assertEqual(expected_value, real_value)
        self.assertEqual(expected_employee, real_employee)

    def test_When_PostMethodOnEditEmployee_Should_ErrorWith405(self):
        response = self.client.post(self.edit_url, {})

        expected_status = status.HTTP_405_METHOD_NOT_ALLOWED
        real_status = response.status_code

        self.assertEqual(expected_status, real_status)

    def test_When_PutMethodOnEditEmployee_Should_ErrorWith405(self):
        response = self.client.put(self.edit_url, {})

        expected_status = status.HTTP_405_METHOD_NOT_ALLOWED
        real_status = response.status_code

        self.assertEqual(expected_status, real_status)

    def test_When_PatchMethodOnEditEmployee_Should_ErrorWith405(self):
        response = self.client.patch(self.edit_url, {})

        expected_status = status.HTTP_405_METHOD_NOT_ALLOWED
        real_status = response.status_code

        self.assertEqual(expected_status, real_status)

    def test_When_DeleteMethodOnEditEmployee_Should_ErrorWith405(self):
        response = self.client.delete(self.edit_url)

        expected_status = status.HTTP_405_METHOD_NOT_ALLOWED
        real_status = response.status_code

        self.assertEqual(expected_status, real_status)

    def test_When_GetMethodOnEditEmployeeWithOutAuth_Should_NoAuthWith200(
            self):
        response = self.client.get(self.edit_url)

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

    def test_When_GetMethodOnSingleEmployeeNotFoundId_Should_NotFoundWith200(
            self):
        client = self.client
        client.force_login(self.user)

        response = client.get(self.edit_url)

        expected_status = status.HTTP_200_OK
        real_status = response.status_code

        expected_data = '\n'.join([
            '<h5 class="card-title">Вы не авторизованы</h5>',
            '<p class="card-text">',
            'Для доступа к данной странице, необходимо быть авторизованным.',
            '</p>',
        ])
        real_data = response.content.decode('utf-8').replace('  ', '')

        expected_not_found = '<h5 class="card-title">Страница не найдена</h5>'
        real_not_found = real_data

        self.assertEqual(expected_status, real_status)
        self.assertNotIn(expected_data, real_data)
        self.assertIn(expected_not_found, real_not_found)

    def test_When_GetMethodOnSingleEmployeeValidId_Should_DataWith200(
            self):
        job_title = JobTitle.objects.create(**{
            'title': 'q' * 50,
        })

        Employee.objects.create(**{
            'id': 1,
            'first_name': 'q' * 50,
            'middle_name': 'q' * 50,
            'last_name': 'q' * 50,
            'wage': 100.0,
            'job_title': job_title,
        })

        client = self.client
        client.force_login(self.user)

        response = client.get(self.edit_url)

        expected_status = status.HTTP_200_OK
        real_status = response.status_code

        expected_data = '<h5 class="card-title">Страница не найдена</h5>'
        real_data = response.content.decode('utf-8').replace('  ', '')

        expected_btn_delete = '\n'.join([
            '<div class="btn btn-danger" id="btn-delete">',
            'Удалить',
            '</div>',
        ])
        real_btn_delete = real_data

        self.assertEqual(expected_status, real_status)
        self.assertNotIn(expected_data, real_data)
        self.assertIn(expected_btn_delete, real_btn_delete)

    def test_When_PostMethodOnCreateEmployee_Should_ErrorWith405(self):
        response = self.client.post(self.create_url, {})

        expected_status = status.HTTP_405_METHOD_NOT_ALLOWED
        real_status = response.status_code

        self.assertEqual(expected_status, real_status)

    def test_When_PutMethodOnCreateEmployee_Should_ErrorWith405(self):
        response = self.client.put(self.create_url, {})

        expected_status = status.HTTP_405_METHOD_NOT_ALLOWED
        real_status = response.status_code

        self.assertEqual(expected_status, real_status)

    def test_When_PatchMethodOnCreateEmployee_Should_ErrorWith405(self):
        response = self.client.patch(self.create_url, {})

        expected_status = status.HTTP_405_METHOD_NOT_ALLOWED
        real_status = response.status_code

        self.assertEqual(expected_status, real_status)

    def test_When_DeleteMethodOnCreateEmployee_Should_ErrorWith405(self):
        response = self.client.delete(self.create_url)

        expected_status = status.HTTP_405_METHOD_NOT_ALLOWED
        real_status = response.status_code

        self.assertEqual(expected_status, real_status)

    def test_When_GetMethodOnCreateEmployeeWithOutAuth_Should_NoAuthWith200(
            self):
        response = self.client.get(self.create_url)

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

    def test_When_GetMethodOnCreateEmployeeWithAuth_Should_DataWith200(self):
        client = self.client
        client.force_login(self.user)

        response = client.get(self.create_url)

        expected_status = status.HTTP_200_OK
        real_status = response.status_code

        expected_data = '\n'.join([
            '<h5 class="card-title">Вы не авторизованы</h5>',
            '<p class="card-text">',
            'Для доступа к данной странице, необходимо быть авторизованным.',
            '</p>',
        ])
        real_data = response.content.decode('utf-8').replace('  ', '')

        expected_not_found = '<h5 class="card-title">Страница не найдена</h5>'
        real_not_found = real_data

        expected_btn_delete = '\n'.join([
            '<div class="btn btn-danger d-none" id="btn-delete">',
            'Удалить',
            '</div>',
        ])
        real_btn_delete = real_data

        self.assertEqual(expected_status, real_status)
        self.assertNotIn(expected_data, real_data)
        self.assertNotIn(expected_not_found, real_not_found)
        self.assertIn(expected_btn_delete, real_btn_delete)
