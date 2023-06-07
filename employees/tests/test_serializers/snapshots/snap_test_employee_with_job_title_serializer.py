# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot

snapshots = Snapshot()

snapshots['EmployeeWithJobTitleSerializerTestCase::test_Should_SpecificFormatForEachField 1'] = '''EmployeeWithJobTitleSerializer():
    id = IntegerField(label='ID', read_only=True)
    first_name = CharField(help_text='Employee first name', max_length=255, required=False)
    middle_name = CharField(help_text='Employee middle name', max_length=255, required=False)
    last_name = CharField(help_text='Employee last name', max_length=255, required=False)
    date_of_receipt = DateField(help_text='Employee date of receipt on job', required=False)
    wage = DecimalField(decimal_places=2, help_text='Employee wage for work', max_digits=12)
    photo = ImageField(required=False)
    job_title = JobTitleSerializer(read_only=True):
        id = IntegerField(label='ID', read_only=True)
        title = CharField(help_text='Job title.', max_length=255, required=False)
    job_title_id = PrimaryKeyRelatedField(queryset=<QuerySet []>, source='job_title', write_only=True)'''
