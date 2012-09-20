from django.db import models
from django.utils.translation import ugettext_lazy as _

class Instances_Config(models.Model):
    name = models.CharField(max_length=128,null=True, blank=True, verbose_name=_('Name'))
    ipaddress = models.CharField(max_length=512, null=True, blank=True, verbose_name=_('IP Address'))
    uuid = models.CharField(max_length=128, null=True, blank=True, unique=True, db_index=True, verbose_name=_('Instance UUID'))
    moniting_state = models.CharField(max_length=1024, null=True, blank=True, verbose_name=_('Moniting State'))
    notification_state = models.CharField(max_length=1024, null=True, blank=True, verbose_name=_('Notification State'))
    
    def __unicode__(self):
        return "[%s %s %s]" % (self.name, self.ipaddress, self.uuid)
    
    class Meta:
        verbose_name = _('Instances_Config')
        verbose_name_plural = _('Instances_Config')
        ordering = ['-name']