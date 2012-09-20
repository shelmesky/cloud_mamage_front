from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import smart_unicode

class SendRuler(models.Model):
    created_time = models.DateTimeField(auto_now_add=True, verbose_name=_('Created Time'))
    time_start = models.DateTimeField(blank=True, null=True, verbose_name=_('Start Time'))
    time_end = models.DateTimeField(blank=True, null=True, verbose_name=_('End Time'))
    service_description = models.CharField(blank=True, null=True, max_length=1024, verbose_name=_('Service Name'))
    
    host_name = models.CharField(max_length=256, verbose_name=_('Host Name'))
    host_name_include = models.CharField(max_length=256, verbose_name=_('Host Name Include'))
    user_name = models.CharField(max_length=256, verbose_name=_('User Name'))
    state = models.CharField(max_length=256, verbose_name=_('State'))
    output = models.CharField(max_length=1024, verbose_name=_('Output'))
    
    def __unicode__(self):
        return ("ID: %s [%s - %s - %s]" % (self.id,self.host_name,self.service_description,self.output))
    
    class Meta:
        verbose_name = _('SendRuler')
        verbose_name_plural = _('SendRuler')
        ordering = ['-created_time']