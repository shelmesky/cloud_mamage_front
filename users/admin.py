from django.contrib import admin
from users.models import Account

class AccountAdmin(admin.ModelAdmin):
    list_display = ('username','password','email','group_name','last_login','is_valid','date_joined')
    search_fields = ('username','email')
    

admin.site.register(Account,AccountAdmin)