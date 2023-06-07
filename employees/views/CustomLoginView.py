from django.contrib.auth.views import LoginView


class CustomLoginView(LoginView):
    template_name = 'login.html'
    next_page = 'employee/'
    redirect_authenticated_user = True
