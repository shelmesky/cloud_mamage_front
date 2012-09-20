import os
from django import template
from django.conf import settings
LOCAL_PATH = settings.LOCAL_PATH


register = template.Library()

global_times_range = ['hours4','hours25','week1','month1','year1']

@register.inclusion_tag('tag/show_service_chart.html', takes_context=False)
def show_service_chart(host, service):
    service = service.replace(' ','_')
    exists = 0
    for ranges in global_times_range:
        if os.path.exists(os.path.join(LOCAL_PATH, 'perfdata' , host, service + '_' + ranges + '.png')):
            exists +=1
    if exists == len(global_times_range):
        return {'show_chart':True,'host':host,'service':service}
    else:
        return {'show_chart':False}