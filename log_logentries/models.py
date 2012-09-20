from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import smart_unicode

class Notification(models.Model):
    hostname = models.CharField(max_length=128, db_index=True, verbose_name=_('Hostname'))
    state = models.IntegerField(max_length=1,verbose_name = _('State'))
    service_description = models.CharField(max_length=128,verbose_name=_('Service Description'))
    notification_type = models.IntegerField(max_length=1,verbose_name = _('Notification_Type'))
    created_time = models.DateTimeField(auto_now_add=True, verbose_name=_('Created Time'))
    output = models.CharField(max_length=1024,verbose_name=_('Notification Output'))
    msg_type = models.CharField(max_length=128,verbose_name=_('Message Type'))
    
    has_processed = models.IntegerField(blank=True, null=True, max_length=1,verbose_name=_('Has Processed'))
    
    def __unicode__(self):
        return ("ID: %s" % (self.id))
    
    class Meta:
        verbose_name = _('Notification')
        verbose_name_plural = _('Notification')
        ordering = ['-created_time']