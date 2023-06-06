from django.contrib import admin

from .models.Employee import Employee
from .models.JobTitle import JobTitle


@admin.register(Employee)
class EmployeeModelAdmin(admin.ModelAdmin):
    pass


@admin.register(JobTitle)
class JobTitleModelAdmin(admin.ModelAdmin):
    pass
