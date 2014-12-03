from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^$', 'monitor.views.index', name='monitor_index'),
    url(r'^dashboard/$', 'monitor.views.dashboard', name='monitor_dashboard'),
)
