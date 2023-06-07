# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot

snapshots = Snapshot()

snapshots['EmployeeSerializerTestCase::test_Should_SpecificFormatForEachField 1'] = '''EmployeeSerializer():
    id = IntegerField(label='ID', read_only=True)
    first_name = CharField(help_text='Employee first name', max_length=255, required=False)
    middle_name = CharField(help_text='Employee middle name', max_length=255, required=False)
    last_name = CharField(help_text='Employee last name', max_length=255, required=False)'''
