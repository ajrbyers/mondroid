from django.conf.urls import patterns, include, url
from django.contrib import admin

from monitor.views import AllMonitorsFeed

urlpatterns = patterns('',
    url(r'^$', 'monitor.views.index', name='monitor_index'),
    url(r'^dashboard/$', 'monitor.views.dashboard', name='monitor_dashboard'),
    url(r'^info/(?P<monitor_id>\d+)/$', 'monitor.views.info', name='old_monitor_info'),
    url(r'^detail/(?P<monitor_id>\d+)/$', 'monitor.views.detail', name='monitor_info'),

    # RSS
    url(r'^rss/$', AllMonitorsFeed()),
    url(r'^rss/(?P<monitor_id>[0-9]+)$', AllMonitorsFeed()),
)
