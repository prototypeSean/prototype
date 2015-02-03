# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('proto_demo', '0002_auto_20150121_1657'),
    ]

    operations = [
        migrations.RenameField(
            model_name='project',
            old_name='project_relate_major',
            new_name='project_request_major',
        ),
    ]
