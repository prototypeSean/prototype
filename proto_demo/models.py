# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import datetime
from django.db import models
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
# Create your models here.

def _upload_path(instance,filename):
    return instance.get_upload_path(filename)

class Category(models.Model):
    category_name = models.CharField(max_length=200)
    #input by administrators and selectable in maker_form& project_form
    def __unicode__(self):
        return self.category_name

class Major(models.Model):
    major_name = models.CharField(max_length=200)
    other_major_tag = models.CharField(max_length=200,blank=True)
    # other_major should be only a field in form than add to Major model
    # input from maker_form and selectable by project_form
    def __unicode__(self):
        return self.major_name

class Maker(models.Model):
    profile_pic = models.ImageField(blank=True,upload_to=_upload_path)
    user = models.OneToOneField(User)
    maker_major = models.ManyToManyField(Major,blank=True)
    maker_other_major = models.CharField(max_length=200,blank=True)
    # how to prevent other_major=maker_major? get or create?
    maker_related_category = models.ManyToManyField(Category)
    # let them choose interested category
    maker_bonus_offer = models.CharField(blank=True,max_length=200)
    # add some tag for themself to improve matching
    maker_detail = RichTextField(config_name='detail')
    def __unicode__(self):
        return self.user.username
    def get_upload_path(self,filename):
        return "maker/"+str(self.user.username)+"/"+filename

class Project(models.Model):
    project_category = models.ForeignKey(Category)
    #because we want maker 'choose' but enter any category
    #match with maker_relate
    project_name = models.CharField(max_length=200)
    project_starter = models.ManyToManyField(User, related_name='starter')
    #current login user
    project_request_major = models.ManyToManyField(Major)
    #match with maker major & other major
    project_matched_maker = models.ManyToManyField(User, related_name='matched_maker')
    pub_date = models.DateTimeField('date published')
    project_detail = RichTextField(config_name='detail')
    project_file = models.FileField(upload_to=_upload_path,blank=True)
    def __unicode__(self):
        return self.project_name

    def get_upload_path(self,filename):
        return "project_uploads/"+str(self.id)+"/"+filename
    # project_uploads前面不用加斜線，會自動接在media資料夾後面產生

