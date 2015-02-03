# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import ckeditor.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('category_name', models.CharField(max_length=200)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Major',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('major_name', models.CharField(max_length=200)),
                ('other_major_tag', models.CharField(max_length=200, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Maker',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('profile_pic', models.ImageField(upload_to=b'profile_pic', blank=True)),
                ('maker_other_major', models.CharField(max_length=200, blank=True)),
                ('maker_bonus_offer', models.CharField(max_length=200, blank=True)),
                ('maker_detail', ckeditor.fields.RichTextField()),
                ('maker_major', models.ManyToManyField(to='proto_demo.Major', blank=True)),
                ('maker_related_category', models.ManyToManyField(to='proto_demo.Category')),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('project_name', models.CharField(max_length=200)),
                ('pub_date', models.DateTimeField(verbose_name=b'date published')),
                ('project_detail', ckeditor.fields.RichTextField()),
                ('project_category', models.ForeignKey(to='proto_demo.Category')),
                ('project_matched_maker', models.ManyToManyField(related_name='matched_maker', to='proto_demo.Maker')),
                ('project_relate_major', models.ManyToManyField(to='proto_demo.Major')),
                ('project_starter', models.ManyToManyField(related_name='starter', to='proto_demo.Maker')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
