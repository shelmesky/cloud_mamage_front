from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

# add tag i18n to template automatic.
from django import template
template.add_to_builtins('django.templatetags.i18n')


urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$',include('users.urls')),
    url(r'^home/$','users.views.home',name='home'),
    url(r'^profile/$','users.views.profile',name='userprofile'),
    url(r'^logout/$','users.views.logout',name='logout'),
    url(r'^host_list/$','host_list.views.host_list',name='host_list'),
    url(r'^service_list/$','service_list.views.service_list',name='service_list'),
    url(r'^system/$','system.views.show_settings',name='system_settings'),
    url(r'^system/getrule$','system.views.get_ruler_list',name='system_getrule'),
    url(r'^system_update/$','system.views.update_settings',name='update_settings'),
    url(r'^notification/',include('notification.urls')),
    url(r'^message',include('log_logentries.urls')),
    url(r'^update_result/$','jobs.views.update_result',name='update_result'),
    url(r'^jobs/',include('jobs.urls')),
    url(r'^instances/',include('instances.urls')),
    url(r'^update/$','process_notification.views.update',name='process_notification'),
    url(r'^revoke/$','process_notification.views.revoke',name='revoke_notification'),
    url(r'^perfdata/(?P<host>[^/]+)/(?P<service>[^/]+)/$', 'perfdata.views.perfdata_host_service', name='perfdata'),
    url(r'^getchart/(?P<host>[^/]+)/(?P<service>[^/]+)/(?P<ranges>[^/]+)/$', 'perfdata.views.get_chart', name='get_chart'),
    url(r'^message/$','message.views.send_message',name='message'),
)
