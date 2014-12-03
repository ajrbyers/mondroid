from django.contrib import admin
from models import *

class MonitorAdmin(admin.ModelAdmin):
    list_display = ('name', 'url', 'current_state')

class CheckAdmin(admin.ModelAdmin):
    list_display = ('monitor', 'status_code', 'elapsed_time', 'up')

class DownTimeAdmin(admin.ModelAdmin):
	list_display = ('monitor', 'active')


admin_list = [
    (Monitor, MonitorAdmin),
    (Check, CheckAdmin),
    (DownTime, DownTimeAdmin),
]

[admin.site.register(*t) for t in admin_list]