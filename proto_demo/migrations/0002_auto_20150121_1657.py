# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('proto_demo', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='project_matched_maker',
            field=models.ManyToManyField(related_name='matched_maker', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='project',
            name='project_starter',
            field=models.ManyToManyField(related_name='starter', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
