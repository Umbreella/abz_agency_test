from django.views.generic.base import TemplateView

from ..models.Employee import Employee


class SingleEmployeeTemplateView(TemplateView):
    template_name = 'single_employee.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['user'] = self.request.user

        employee_id = kwargs.get('pk')

        context['operation'] = 'edit' if employee_id else 'create'
        context['employee'] = Employee.objects.filter(**{
            'id': employee_id
        }).first()

        return context
