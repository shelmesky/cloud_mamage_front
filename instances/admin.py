from django.contrib import admin
from instances.models import Instances_Config

class InstancesConfigAdmin(admin.ModelAdmin):
    list_display = ('name','ipaddress','uuid','moniting_state','notification_state')
    search_fields = ('name','uuid')

admin.site.register(Instances_Config, InstancesConfigAdmin)