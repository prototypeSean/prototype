from django.conf.urls import patterns, include, url
from django.contrib import admin
from views import media_view


urlpatterns = patterns('',
    # Examples:

    # url(r'^blog/', include('blog.urls')),
    url(r'^ckeditor/', include('ckeditor.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^demo/', include('proto_demo.urls', namespace = 'proto_demo')),
    url(r'^media/(?P<path>.*)', media_view),


    #include means proto_demo.urls take control for every url after demo/
#---------------------python social auth---------------------------------------------
#    url(r'^$', 'example.views.home'),
#    url(r'^admin/', include(admin.site.urls)),
#    url(r'^email-sent/', 'example.views.validation_sent'),
#    url(r'^login/$', 'example.views.home'),
#    url(r'^logout/$', 'example.views.logout'),
#    url(r'^done/$', 'example.views.done', name='done'),
#    url(r'^ajax-auth/(?P<backend>[^/]+)/$', 'example.views.ajax_auth',
#        name='ajax-auth'),
#    url(r'^email/$', 'example.views.require_email', name='require_email'),
#    url(r'', include('social.apps.django_app.urls', namespace='social'))
#---------------------python social auth---------------------------------------------

)
