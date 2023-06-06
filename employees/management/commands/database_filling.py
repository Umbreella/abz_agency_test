import random

from alive_progress import alive_bar
from django.core.management import BaseCommand
from django.db import transaction
from faker import Faker

from ...models.Employee import Employee
from ...models.JobTitle import JobTitle


class Command(BaseCommand):
    help = f'Filling database more than {50_000} rows for employee table.'

    @transaction.atomic()
    def handle(self, *args, **options):
        faker = Faker()
        count_employee = 10_000
        count_job_title = 100

        job_titles = []
        with alive_bar(count_job_title) as bar:
            print('Filling job_title ...')
            for _ in range(count_job_title):
                job_titles.append(
                    JobTitle(**{
                        'title': faker.job(),
                    })
                )
                bar()

        JobTitle.objects.bulk_create(job_titles)

        first_layer_employee = []
        with alive_bar(count_employee) as bar:
            print('Filling first_layer_employee ...')
            for _ in range(count_employee):
                first_layer_employee.append(
                    Employee(**{
                        'first_name': faker.first_name(),
                        'middle_name': faker.first_name(),
                        'last_name': faker.last_name(),
                        'date_of_receipt': faker.date_this_century(),
                        'wage': random.uniform(10_000, 100_000),
                        'job_title': random.choice(job_titles),
                    })
                )
                bar()

        Employee.objects.bulk_create(first_layer_employee)

        second_layer_employee = []
        with alive_bar(count_employee) as bar:
            print('Filling second_layer_employee ...')
            for _ in range(count_employee):
                second_layer_employee.append(
                    Employee(**{
                        'first_name': faker.first_name(),
                        'middle_name': faker.first_name(),
                        'last_name': faker.last_name(),
                        'date_of_receipt': faker.date_this_century(),
                        'wage': random.uniform(10_000, 100_000),
                        'job_title': random.choice(job_titles),
                        'boss': random.choice(first_layer_employee),
                    })
                )
                bar()

        Employee.objects.bulk_create(second_layer_employee)

        third_layer_employee = []
        with alive_bar(count_employee) as bar:
            print('Filling third_layer_employee ...')
            for _ in range(count_employee):
                third_layer_employee.append(
                    Employee(**{
                        'first_name': faker.first_name(),
                        'middle_name': faker.first_name(),
                        'last_name': faker.last_name(),
                        'date_of_receipt': faker.date_this_century(),
                        'wage': random.uniform(10_000, 100_000),
                        'job_title': random.choice(job_titles),
                        'boss': random.choice(second_layer_employee),
                    })
                )
                bar()

        Employee.objects.bulk_create(third_layer_employee)

        fourth_layer_employee = []
        with alive_bar(count_employee) as bar:
            print('Filling fourth_layer_employee ...')
            for _ in range(count_employee):
                fourth_layer_employee.append(
                    Employee(**{
                        'first_name': faker.first_name(),
                        'middle_name': faker.first_name(),
                        'last_name': faker.last_name(),
                        'date_of_receipt': faker.date_this_century(),
                        'wage': random.uniform(10_000, 100_000),
                        'job_title': random.choice(job_titles),
                        'boss': random.choice(third_layer_employee),
                    })
                )
                bar()

        Employee.objects.bulk_create(fourth_layer_employee)

        fifth_layer_employee = []
        with alive_bar(count_employee) as bar:
            print('Filling fifth_layer_employee ...')
            for _ in range(count_employee):
                fifth_layer_employee.append(
                    Employee(**{
                        'first_name': faker.first_name(),
                        'middle_name': faker.first_name(),
                        'last_name': faker.last_name(),
                        'date_of_receipt': faker.date_this_century(),
                        'wage': random.uniform(10_000, 100_000),
                        'job_title': random.choice(job_titles),
                        'boss': random.choice(fourth_layer_employee),
                    })
                )
                bar()

        Employee.objects.bulk_create(fifth_layer_employee)

        print('DataBase is filling!')
