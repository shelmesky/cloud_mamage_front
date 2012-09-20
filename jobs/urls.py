from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('jobs.views',
    url('owner_job/$', 'owner_job', name='owner_job'),
    url('dispatched_job/$', 'dispatched_job', name='dispatched_job'),
)