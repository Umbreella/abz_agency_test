from django.db import models


class JobTitle(models.Model):
    title = models.CharField(**{
        'max_length': 255,
        'default': '',
        'help_text': 'Job title.',
    })

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
