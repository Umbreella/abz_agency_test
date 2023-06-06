from django.views.generic.base import TemplateView


class EmployeeTemplateView(TemplateView):
    template_name = 'employee_table.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(*kwargs)

        context['user'] = self.request.user

        return context
