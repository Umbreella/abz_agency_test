"""
URL configuration for abz_agency project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib.auth.views import LogoutView
from django.urls import path

from .views.CustomLoginView import CustomLoginView
from .views.EmployeeTemplateView import EmployeeTemplateView
from .views.EmployeeViewSet import EmployeeViewSet
from .views.JobTitleViewSet import JobTitleViewSet
from .views.SingleEmployeeTemplateView import SingleEmployeeTemplateView

urlpatterns = [
    path(**{
        'route': 'login/',
        'view': CustomLoginView.as_view(),
        'name': 'login',
    }),
    path(**{
        'route': 'logout/',
        'view': LogoutView.as_view(),
        'name': 'logout',
    }),
    path(**{
        'route': '',
        'view': EmployeeTemplateView.as_view(),
        'name': 'employee_template',
    }),
    path(**{
        'route': 'employee/<int:pk>/',
        'view': SingleEmployeeTemplateView.as_view(),
        'name': 'edit_employee_template',
    }),
    path(**{
        'route': 'employee/create/',
        'view': SingleEmployeeTemplateView.as_view(),
        'name': 'create_employee_template',
    }),
    path(**{
        'route': 'api/employee/',
        'view': EmployeeViewSet.as_view({
            'get': 'list',
            'post': 'create',
        }),
        'name': 'list_employee',
    }),
    path(**{
        'route': 'api/employee/<int:pk>/',
        'view': EmployeeViewSet.as_view({
            'get': 'retrieve',
            'put': 'update',
            'patch': 'partial_update',
            'delete': 'destroy',
        }),
        'name': 'single_employee',
    }),
    path(**{
        'route': 'api/jobtitle/',
        'view': JobTitleViewSet.as_view({
            'get': 'list',
        }),
        'name': 'list_jobtitle',
    }),
]
