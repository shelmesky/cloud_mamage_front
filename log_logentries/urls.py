from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('log_logentries.views',
    url('send/$', 'receive_notification', name='send'),
    url('check/$', 'check_md5', name='check_md5'),
)