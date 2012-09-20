from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import smart_unicode
from users.conf.settings import Groups

class Account(models.Model):
    username = models.CharField(blank=True, unique=True, primary_key = True, max_length = 128, help_text=_('Username'))
    password = models.CharField(blank=True, null=True, max_length = 256, help_text=_('Password'))
    email = models.EmailField(blank=True, null=True, help_text = _('Email Address'))
    group_name = models.CharField(blank=True, null=True, max_length = 32, choices = Groups, help_text=_('Group Name'))
    last_login = models.IPAddressField(blank=True, null=True, help_text=_('Last Login IP'))
    is_valid = models.NullBooleanField(blank=True, null=True, help_text=_('Is User Valid'))
    date_joined = models.DateTimeField(auto_now_add = True, help_text=_('Date Joined'))
    cell_phone = models.CharField(blank=True, null=True, max_length = 256, help_text=_('Cell Phone'))
    
    class Meta:
        verbose_name = _('Account')
        verbose_name_plural = _('Account')
        ordering = ['-date_joined']

