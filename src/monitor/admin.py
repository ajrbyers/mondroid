from django.contrib import admin
from models import *

class MonitorAdmin(admin.ModelAdmin):
    list_display = ('name', 'url', 'current_state')

class CheckAdmin(admin.ModelAdmin):
    list_display = ('monitor', 'elapsed_time', 'capture', 'up')
    readonly_fields = ("capture",)
    list_filter = ('monitor', 'up', 'capture')

admin_list = [
    (Monitor, MonitorAdmin),
    (Check, CheckAdmin),
]

[admin.site.register(*t) for t in admin_list]
