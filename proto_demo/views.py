# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.core.files.storage import default_storage
from django.shortcuts import get_object_or_404, render,redirect
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models.fields.files import FieldFile
from django.views.generic import FormView
from django.views.generic.base import TemplateView
from django.contrib import messages
from django.views.generic import DetailView,ListView
from django.utils.timezone import datetime
from models import Project,Maker,Major,User
from forms import ContactForm, FilesForm, ContactFormSet,StartProjectForm,NewMakerForm,\
    MakerProfileForm,LoginForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
# http://yuji.wordpress.com/2013/01/30/django-form-field-in-initial-data-requires-a-fieldfile-instance/
#test


class FakeField(object):
    storage = default_storage


fieldfile = FieldFile(None, FakeField, 'dummy.txt')


class HomePageView(TemplateView):
    template_name = 'proto_demo/home.html'

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        messages.info(self.request, 'This is a demo of a message.')
        return context


class DefaultFormsetView(FormView):
    template_name = 'proto_demo/formset.html'
    form_class = ContactFormSet


class DefaultFormView(FormView):
    template_name = 'proto_demo/form.html'
    form_class = ContactForm


class DefaultFormByFieldView(FormView):
    template_name = 'proto_demo/form_by_field.html'
    form_class = ContactForm


class FormHorizontalView(FormView):
    template_name = 'proto_demo/form_horizontal.html'
    form_class = ContactForm


class FormInlineView(FormView):
    template_name = 'proto_demo/form_inline.html'
    form_class = ContactForm


class FormWithFilesView(FormView):
    template_name = 'proto_demo/form_with_files.html'
    form_class = FilesForm

    def get_context_data(self, **kwargs):
        context = super(FormWithFilesView, self).get_context_data(**kwargs)
        context['layout'] = self.request.GET.get('layout', 'vertical')
        return context

    def get_initial(self):
        return {
            'file4': fieldfile,
        }

class PaginationView(TemplateView):
    template_name = 'proto_demo/pagination.html'

    def get_context_data(self, **kwargs):
        context = super(PaginationView, self).get_context_data(**kwargs)
        lines = []
        for i in range(10000):
            lines.append('Line %s' % (i + 1))
        paginator = Paginator(lines, 10)
        page = self.request.GET.get('page')
        try:
            show_lines = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            show_lines = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            show_lines = paginator.page(paginator.num_pages)
        context['lines'] = show_lines
        return context


class MiscView(TemplateView):
    template_name = 'proto_demo/misc.html'

#-------------------------------------------------Prototype View----------------------------------------------

def NewMakerView(request):
# A boolean value for telling the template whether the registration was successful.
    # Set to False initially. Code changes value to True when registration succeeds.
    registered = False

    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and UserProfileForm.
        user_form = NewMakerForm(data=request.POST)
        profile_form = MakerProfileForm(data=request.POST,)
        # If the two forms are valid...
        if user_form.is_valid() and profile_form.is_valid():
            # Save the user's form data to the database.
            user = user_form.save()
            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            user.set_password(user.password)
            user.save()
            # Now sort out the UserProfile instance.
            # Since we need to set the user attribute ourselves, we set commit=False.
            # This delays saving the model until we're ready to avoid integrity problems.
            profile = profile_form.save(commit=False)
            profile.user = user
            # Did the user provide a profile picture?
            # If so, we need to get it from the input form and put it in the UserProfile model.
            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']
            # Now we save the UserProfile model instance.
            profile.save()
            profile_form.save_m2m()
                            #major = Major.objects.get(major_name=profile_form.cleaned_data['other_major'])
                            #profile.maker_major.add(major)
                            #如果other_major不存在maker表格裡面才要加上面兩行
            # Update our variable to tell the template registration was successful.
            registered = True
        # Invalid form or forms - mistakes or something else?
        # Print problems to the terminal.
        # They'll also be shown to the user.
        else:
            print user_form.errors, profile_form.errors

    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    else:
        user_form = NewMakerForm()
        profile_form = MakerProfileForm()

    # Render the template depending on the context.
    return render(request,
            'proto_demo/register.html',
            {'user_form': user_form, 'profile_form': profile_form, 'registered': registered} )

def user_login(request):
    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        # Gather the username and password provided by the user.
        # This information is obtained from the login form.
        username = request.POST.get('username')
        password = request.POST.get('password')
        # Use Django's machinery to attempt to see if the username/password
        # combination is valid - a User object is returned if it is.
        user = authenticate(username=username, password=password)
        # If we have a User object, the details are correct.
        # If None (Python's way of representing the absence of a value), no user
        # with matching credentials was found.
        if user:
            # Is the account active? It could have been disabled.
            if user.is_active:
                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage.
                login(request, user)
                return HttpResponseRedirect(request.POST.get('next',''))
            else:
                # An inactive account was used - no logging in!
                return HttpResponse("Your account is disabled.")
        else:
            # Bad login details were provided. So we can't log the user in.
            print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponse("Invalid login details supplied.")
    # The request is not a HTTP POST, so display the login form.
    # This scenario would most likely be a HTTP GET.
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        return render(request, 'proto_demo/login.html', {'login_form':LoginForm,'next': request.GET.get('next','')})


@login_required
def MakerProfileView(request,pk):
        maker = get_object_or_404(Maker,pk = pk)
        return render(request,'proto_demo/maker_profile.html',{'maker':maker})


@login_required
def StartProjectFormView(request):
    if request.method == "POST":
        form = StartProjectForm(request.POST,)
        #form with data
        if form.is_valid():
            project_form = form.save(commit=False)
            project_form.pub_date = datetime.now()
            project_form.save()
            project_form.project_starter.add(request.user)
            # project_form.project_maker 這樣其實會被轉成一個 select
            # this is how you should use m2m field!!!!!!!!!
            form.save_m2m()
            #don't use project_form here! USE form
            #form.save() 之後回傳的東西是 model model 沒法再save_m2m()
            return redirect('proto_demo:project_status', pk=project_form.pk)
    else:
        form = StartProjectForm()
        #empty form
    return render(request, 'proto_demo/start_project.html', {'form': form,})


@login_required
def ProjectStatusView(request,pk):
    '''
     表格Project 已經存在,要從使用者輸入的"project_request_major"做配對
    *需求1 選出所有maker之中 major欄位含有 project_request_major 的任何maker
    *需求2 顯示順序依照配對成功的數量降冪排序
    *需求3 只顯示項目有需求的major,也就是 project_request_major 與 maker_major 的交集
    '''
    project = get_object_or_404(Project, pk=pk)
    # 從使用者需求的網址<pk> 取得要讀取哪個Project的 row
    relatemaker = Maker.objects.filter(maker_major__in=project.project_request_major.all())
    # 從 Maker 表格裡面 拉出 majro欄位中 包含project.project_request_major 的所有人
    relatemaker = list(set(relatemaker))
    #用set 把重複的剃除
    relatemaker_i_majro = []
    #開一個空的list,等下要儲存(append)每個使用者交集的結果,因為要有順序,所以要用list
    p_request_major = project.project_request_major.all()
    # 先把 project_request_major 做成 QuetySet 丟進變數,等下做交集的時候會用到

    #接下來要做每個maker的 maker_major 與 request_major的交集,所以用for把每個maker拉出來,再檢索他的maker_major
    for r_m in relatemaker:
        rm = Maker.objects.get(user=r_m)
        rm_major = Major.objects.filter(maker__user=rm).all()
        # **r_major = Maker.objects.filter(user=r_m).values_list('maker_major__major_name')
        # 用values_list 取m2m欄位__major_name !!!注意！！！maker_major__major_name　這種用法正反向m2m都通用！！
        # **這行等於上面兩行,但是傳回的東西不同 因為我要她傳回querset所以不能用values_list
        rm_inter_major =  rm_major&p_request_major
        # 這邊就知道為啥一定要他回傳queryset了 因為要做交集,不一樣的格式會變成空集合
        relatemaker_i_majro.append(rm_inter_major)
        # *extend = 延伸原本的list = 維持1 個 list
        # *append = 在原本的list 插入 一個子 list
        # 排序要照著配對條件多寡的順序 rm_inter_major
        # 但是顯示還是要顯示全部的 rm_major 這部分在從 template裡面拉就可以
    result = dict(zip(relatemaker, relatemaker_i_majro))
    #把 relatemaker 人名 跟 交集的 rm_inter_major 合併為一個dict

    result = sorted(result,key=lambda k:len(result[k]),reverse=True)
    #依照這個 dict 的 values長度 做排序 (因為dict本身沒有順序 所以輸出還是一個list *OrderedDict不知道為啥不能用)
    #至此 result 輸出的就是 依照配對成功條件降冪排序的 maker 然後顯示maker_major 的部分在template裡面完成

    # **lambda用法:
    # 以relatemaker_majro 的多寡排序=>sorted方法參照 key, key=建立一個匿名功能 參數是 k , k 帶入函式 len(result[k])

    return render(request, 'proto_demo/projectstatus.html', {'project': project,
                                                             'relatemaker':relatemaker,
                                                             'relatemaker_i_majro':relatemaker_i_majro, #沒用到
                                                             'result':result,
                                                             'p_request_major':p_request_major,
                                                             })



@login_required
def MakerBlogView(request,pk):
    return render(request, 'proto_demo/maker_blog.html')


def Match(object):
    pass


@login_required
def restricted(request):
    return HttpResponse("Since you're logged in, you can see this text!")


@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)
    # Take the user back to the homepage.
    return HttpResponseRedirect('../')