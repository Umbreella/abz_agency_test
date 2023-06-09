# Test task - "abz.agency"

![python](https://img.shields.io/badge/python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![django](https://img.shields.io/badge/django-092E20?style=for-the-badge&logo=django&logoColor=white)
![drf](https://img.shields.io/badge/django_rest_framework-A30000?style=for-the-badge&logo=django&logoColor=white)
![html5](https://img.shields.io/badge/html5-E34F26?style=for-the-badge&logo=html5&logoColor=white)
![css3](https://img.shields.io/badge/css3-1572B6?style=for-the-badge&logo=css3&logoColor=white)
![jss](https://img.shields.io/badge/jss-F7DF1E?style=for-the-badge&logo=jss&logoColor=white)
![bootstrap](https://img.shields.io/badge/bootstrap-7952B3?logo=bootstrap&logoColor=white&style=for-the-badge)

### Testing

![unittest](https://img.shields.io/badge/unittest-092E20?style=for-the-badge&logo=pytest&logoColor=white)
![codecov](https://img.shields.io/codecov/c/github/Umbreella/abz_agency_test?style=for-the-badge&logo=codecov)

## Description

[Task Description](TaskDescription.pdf)

Completed items:

1. Part 1:
    1. :white_check_mark: Information about every employee stored in Database:
        1. First name / Last name / Middle name
        2. Job title
        3. Date of receipt
        4. Salary mount
    2. :white_check_mark: Every employee has a boss
    3. :white_check_mark: Database has more than 50.000 employees
2. Part 2:
    1. :white_check_mark: Creating a database based on migrations
    2. :white_check_mark: [Faker](https://faker.readthedocs.io/en/master/) was
       used to populate the database
    3. :white_check_mark: Bootstrap is included
    4. :white_check_mark: Page with list of employee with ability to sort by
       all fields
    5. :white_check_mark: Add search by all fields
    6. :white_check_mark: Add order by all fields
    7. :white_check_mark: Add session authentication
    8. :white_check_mark: All pages only for authentication user
    9. :white_check_mark: Add page with CRUD for employee
    10. :white_check_mark: Add upload file and img in list of employee
    11. :white_check_mark: Add lazy load for list of employee
    12. :white_check_mark: Add Drag&Drop

## Getting Started

### Dependencies

![postgresql](https://img.shields.io/badge/postgresql-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)

### Environment variables

* To run the application, you have to perform one of the options:
    * specify the **environment variables**
    * overwrite **.env** file
* The list of all environment variables is specified in the **[.env](.env)**

## Docker

1. docker-compose.yml

```docker
version: "3"

services:
  abz_agency_test:
    image: umbreella/abz_agency_test:latest
    ports:
      - [your_open_port]:8000
    env_file:
      - [path_to_env_file]
    volumes:
      - [path_to_static_folder]:/usr/src/app/static/
      - [path_to_media_folder]:/usr/src/app/media/
```

* Docker-compose run

```commandline
docker-compose up -d
```

* Open bash in container

```commandline
docker exec --it abz_agency_test bash
```

* Run commands

```commandline
python manage.py collectstatic
python manage.py migrate
python manage.py database_filling
python manage.py createsuperuser
```

## Endpoints

* Login page

```commandline
[your_ip_address]/
```

* Employee table

```commandline
[your_ip_address]/employee/
```

* API docs

```commandline
[your_ip_address]/api/docs/
```

## Live Demo

* [https://abzagency.umbreella-dev.ru/](https://abzagency.umbreella-dev.ru/)
