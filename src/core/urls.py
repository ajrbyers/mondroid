from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^$', 'monitor.views.index', name='mondroid_index'),
    url(r'^login/$', 'monitor.views.user_login', name='user_login'),
    url(r'^logout/$', 'monitor.views.user_logout', name='user_logout'),
    url(r'^monitor/', include('monitor.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
