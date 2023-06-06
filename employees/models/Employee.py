from django.db import models
from django.utils import timezone

from .JobTitle import JobTitle


class Employee(models.Model):
    first_name = models.CharField(max_length=255, default='')
    middle_name = models.CharField(max_length=255, default='')
    last_name = models.CharField(max_length=255, default='')
    job_title = models.ForeignKey(JobTitle, on_delete=models.CASCADE)
    date_of_receipt = models.DateField(default=timezone.now)
    wage = models.DecimalField(max_digits=12, decimal_places=2)
    boss = models.ForeignKey('self', default=None, null=True,
                             on_delete=models.SET_NULL, blank=True)
    photo = models.ImageField(upload_to='employee/%Y/%m/%d', null=True,
                              blank=True)

    def save(self, *args, **kwargs):
        if isinstance(self.wage, float):
            self.wage = str(round(self.wage, 2))

        self.full_clean()
        super().save(*args, **kwargs)
