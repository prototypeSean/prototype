# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import patterns, url, include
import views
from views import HomePageView, FormHorizontalView, FormInlineView, PaginationView, FormWithFilesView, \
    DefaultFormView, MiscView, DefaultFormsetView, DefaultFormByFieldView
# Uncomment the next two lines to enable the admin:
#from django.contrib import admin
#admin.autodiscover()

# urlpatterns = patterns('',
#     # Examples:
#     # url(r'^$', 'demo.views.home', name='home'),
#     # url(r'^demo/', include('demo.foo.urls')),
#
#     # Uncomment the admin/doc line below to enable admin documentation:
#     # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
#
#     # Uncomment the next line to enable the admin:
#     # url(r'^admin/', include(admin.site.urls)),
# )

urlpatterns = patterns('',
    url(r'^$', HomePageView.as_view(), name='home'),
    url(r'^formset$', DefaultFormsetView.as_view(), name='formset_default'),
    url(r'^form$', DefaultFormView.as_view(), name='form_default'),
    url(r'^form_by_field$', DefaultFormByFieldView.as_view(), name='form_by_field'),
    url(r'^form_horizontal$', FormHorizontalView.as_view(), name='form_horizontal'),
    url(r'^form_inline$', FormInlineView.as_view(), name='form_inline'),
    url(r'^form_with_files$', FormWithFilesView.as_view(), name='form_with_files'),
    url(r'^pagination$', PaginationView.as_view(), name='pagination'),
    url(r'^misc$', MiscView.as_view(), name='misc'),

    url(r'^newmaker/$',views.NewMakerView, name='create_new_maker'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^yourprofile/(?P<pk>\d+)$', views.MakerProfileView, name='maker_profile'),
    url(r'^newproject$',views.StartProjectFormView, name='start_project'),
    url(r'^pstatus/(?P<pk>\d+)$', views.ProjectStatusView, name='project_status'),
    url(r'^makerblog/(?P<pk>\d+)$', views.MakerBlogView, name='maker_blog'),

    url(r'^restricted/', views.restricted, name='restricted'),
    url(r'^logout/$', views.user_logout, name='logout'),


    url(r'^(?P<project_id>\d+)/match$', views.Match, name='match'),



#    url(r'^weblog/', include('zinnia.urls', namespace='zinnia')),
#    url(r'^comments/', include('django_comments.urls')),
#    url(r'^index$',IndexView.as_view(),),
)
