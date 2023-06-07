from django.db import models
from django.utils import timezone

from .JobTitle import JobTitle


class Employee(models.Model):
    first_name = models.CharField(**{
        'max_length': 255,
        'default': '',
        'help_text': 'Employee first name',
    })
    middle_name = models.CharField(**{
        'max_length': 255,
        'default': '',
        'help_text': 'Employee middle name',
    })
    last_name = models.CharField(**{
        'max_length': 255,
        'default': '',
        'help_text': 'Employee last name',
    })
    date_of_receipt = models.DateField(**{
        'default': timezone.now,
        'help_text': 'Employee date of receipt on job',
    })
    wage = models.DecimalField(**{
        'max_digits': 12,
        'decimal_places': 2,
        'help_text': 'Employee wage for work',
    })
    job_title = models.ForeignKey(**{
        'to': JobTitle,
        'on_delete': models.CASCADE,
        'help_text': 'Employee job title',
    })
    boss = models.ForeignKey(**{
        'to': 'self',
        'default': None,
        'null': True,
        'blank': True,
        'on_delete': models.SET_NULL,
        'help_text': 'Employee boss',
    })
    photo = models.ImageField(**{
        'upload_to': 'employee/%Y/%m/%d',
        'null': True,
        'blank': True,
        'help_text': 'Employee photo',
    })

    def save(self, *args, **kwargs):
        if isinstance(self.wage, float):
            self.wage = str(round(self.wage, 2))

        self.full_clean()
        super().save(*args, **kwargs)
