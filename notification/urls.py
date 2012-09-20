from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('notification.views',
    url('^$', 'show_notification', name='notifications'),
    url('search/$', 'advanced_search', name='advanced_search'),
    url('search_result/$', 'advanced_search_result', name='advanced_search_result'),
)