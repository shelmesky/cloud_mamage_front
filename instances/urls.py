from django.conf.urls.defaults import  patterns, include, url

urlpatterns = patterns('instances.views',
    url('^$', 'instances_detail', name='instances-detail'),
    url('^list/$','instances_list',name='instances-list'),
    url('^setting/(?P<uuid>[^/]+)/$', 'instances_setting', name='instances_setting'),
    url('^get_config/$','instances_config',name='instances-config'),
    url('^get_instance_state/$','get_instance_state',name='get_instance_state'),
)