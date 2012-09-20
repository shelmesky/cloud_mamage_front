from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import smart_unicode

class Notification_Result(models.Model):
    time = models.DateTimeField(auto_now_add=True, verbose_name=_('Time Admin To OP'))
    from_user = models.CharField(max_length=128,verbose_name = _('Admin User'))
    to_user = models.CharField(max_length=128, db_index=True, verbose_name=_('OP User'))
    result = models.CharField(max_length=256,verbose_name=_('Admin Result'))
    notification_id = models.IntegerField(max_length=256,verbose_name=_('Notification ID'))
    message_md5 = models.CharField(max_length=64,verbose_name = _('MD5 Signature Of Noti'))
    op_processed_result = models.CharField(blank=True, null=True, max_length=256,verbose_name=_('OP Porcessed Result'))

    class Meta:
        verbose_name = _('Notification_Result')
        verbose_name_plural = _('Notification_Result')
        ordering = ['-time']