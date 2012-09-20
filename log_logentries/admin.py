from django.contrib import admin
from log_logentries.models import Notification

class NotificationAdmin(admin.ModelAdmin):
    list_display = ('id','created_time','hostname','state','service_description','output','has_processed')
    search_fields = ('hostname','service_description','output')

admin.site.register(Notification,NotificationAdmin)