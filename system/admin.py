from django.contrib import admin
from system.models import SendRuler

class SendRulerAdmin(admin.ModelAdmin):
    list_display = ('created_time','host_name','host_name_include','state','output')
    search_fields = ('host_name','host_name_include','output','output')

admin.site.register(SendRuler, SendRulerAdmin)