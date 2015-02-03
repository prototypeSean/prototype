# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms
from django.forms.formsets import BaseFormSet, formset_factory
from bootstrap3.tests import TestForm
from models import Project,Maker,Major,User
from ckeditor.widgets import CKEditorWidget
#from django.utils.translation import ugettext_lazy as _

RADIO_CHOICES = (
    ('1', 'Radio 1'),
    ('2', 'Radio 2'),
)

MEDIA_CHOICES = (
    ('Audio', (
        ('vinyl', 'Vinyl'),
        ('cd', 'CD'),
    )
    ),
    ('Video', (
        ('vhs', 'VHS Tape'),
        ('dvd', 'DVD'),
    )
    ),
    ('unknown', 'Unknown'),
)
#----------------------------------------------PROTOTYPE-------------------------------------------------------------


class NewMakerForm(forms.ModelForm):
    password = forms.CharField(label='密碼')
    username = forms.CharField(help_text='',label='帳號')
#    profile_pic = forms.ImageField()
    #要怎麼把maker form 的 profile_pic加到這裡?
    def __init__(self ,*args, **kwargs):
        super(NewMakerForm,self).__init__(*args, **kwargs)
        # we want to modify the fields.required attribute in this form,so we need to change it's __init__ attribute
        # to do so we need to use super method as see
        # Always use super(cls, self) for Python 2.x or super() for Python 3.x
        # to call the original implementation of a method
        self.fields['first_name'].required = True
        self.fields['email'].required = True
    class Meta:
        model = User
        fields = ('username','password','first_name','last_name','email')
        labels = {
            'first_name':'姓名',
            'profile_pic':'個人圖像',
        }

        widgets = {
            'username':forms.TextInput(attrs={'autocomplete':'off','placeholder': '必要的。小於 30 個字, 只包含字母、數字和 @ . + - _'}),
            'email':forms.TextInput(attrs={'autocomplete':'off',}),
            'password':forms.TextInput(attrs={'autocomplete':'off',}),
            'first_name':forms.TextInput(attrs={'placeholder': '該怎麼稱呼您?',}),
        }

#    def clean(self, *args, **kwargs):
#        super(NewMakerForm,self).clean()
#        pic, = Maker.objects.get_or_create(profile_pic=self.cleaned_data.get('profile_pic'))
#        self.cleaned_data['profile_pic'] = pic.profile_pic


class MakerProfileForm(forms.ModelForm):
    class Meta:
        model = Maker
        fields = ('maker_major','maker_other_major','maker_bonus_offer','maker_related_category',
                  'profile_pic','maker_detail')
        labels = {
            'maker_major':'專業領域',
            'maker_other_major':'其他專業',
            'maker_related_category':'興趣分類',
            'maker_bonus_offer':'Bonus！',
            'maker_detail':'關於自己',
        }
        widgets={
            'maker_major':forms.CheckboxSelectMultiple(attrs={'placeholder':'選擇一項大領域'}),
            'maker_other_major':forms.TextInput(attrs={'placeholder':'較精確地填寫您擅長的領域'}),
            'maker_related_category':forms.CheckboxSelectMultiple(attrs={'placeholder':'有興趣參與的本站分類'}),
            'maker_bonus_offer':forms.TextInput(attrs={'placeholder':'其他您擁有,或可以提供的特點. EX:場地,工具,服務..'}),
            'maker_detail':CKEditorWidget(attrs={'placeholder':'在此處盡可能得清楚表達您的想法、希望發起或參與的項目、或任何有助於您表達自己的介紹'})
        }
    def clean(self, *args, **kwargs):
        super(MakerProfileForm,self).clean()
        major, _ = Major.objects.get_or_create(major_name=self.cleaned_data.get('maker_other_major'))
        # 從 model.Major中用 get_or_create 找尋 major_name 這個欄位, 有沒有跟使用者輸入的 'other_major' 欄位一樣
        # 的文字, 這邊要用 cleaned_data 因為直接get 會得到 "form 欄位的宣告" 而不是裡面的值
        # 因為 get_or_create() 方法會得到一組 tuple (get或create的值,布林), 所以這邊要用 (major,_) = ...
        # major,才會等於我們獲取的物件
        self.cleaned_data['maker_other_major'] = major.major_name

        #一定要用super,因為  The ModelForm.clean() method sets a flag that makes the model
        # validation step validate the uniqueness of model fields that are marked as unique,
        # unique_together or unique_for_date|month|year.
        #If you would like to override the clean() method and maintain this validation,
        # you must call the parent class’s clean() method.


class StartProjectForm(forms.ModelForm):

    class Meta:
        model = Project
        fields = ('project_category','project_name','project_request_major','project_detail')
        widgets = {
            'project_detail':CKEditorWidget(),
            'project_request_major':forms.CheckboxSelectMultiple(),
        }
        labels = {
            'project_category':'項目分類',
            'project_name':'項目名稱',
            'project_request_major':'需求領域',
            'project_detail':'項目細節'
        }

class LoginForm(forms.Form):
    User_Name = forms.CharField(
        widget=forms.TextInput(
            attrs={'name':'username'}
            # attrs here means the html attributes in <input> like name, value...
            # so this 'name' attribute here is for login view to check
            # username = request.POST.get('username')
        )
    )
    Password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'name':'password'}
        )
    )




#----------------------------------------------PROTOTYPE-------------------------------------------------------------
class ContactForm(TestForm):
    pass


class ContactBaseFormSet(BaseFormSet):
    def add_fields(self, form, index):
        super(ContactBaseFormSet, self).add_fields(form, index)

    def clean(self):
        super(ContactBaseFormSet, self).clean()
        raise forms.ValidationError("This error was added to show the non form errors styling")

ContactFormSet = formset_factory(TestForm, formset=ContactBaseFormSet,
                                 extra=2,
                                 max_num=4,
                                 validate_max=True)


class FilesForm(forms.Form):
    text1 = forms.CharField()
    file1 = forms.FileField()
    file2 = forms.FileField(required=False)
    file3 = forms.FileField(widget=forms.ClearableFileInput)
    file4 = forms.FileField(required=False, widget=forms.ClearableFileInput)


class ArticleForm(forms.Form):
    title = forms.CharField()
    pub_date = forms.DateField()
    def clean(self):
        cleaned_data = super(ArticleForm, self).clean()
        raise forms.ValidationError("This error was added to show the non field errors styling.")
        return cleaned_data
