from django.contrib import admin
from process_notification.models import Notification_Result

class Notification_Result_Admin(admin.ModelAdmin):
    list_display = ('time','from_user','to_user','result','op_processed_result')
    search_fields=  ('from_user','to_user','result','op_processed_result')

admin.site.register(Notification_Result,Notification_Result_Admin)