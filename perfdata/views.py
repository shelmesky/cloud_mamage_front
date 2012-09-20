#coding=utf-8
import os
from django.http import HttpResponse
from common.performe_raw_sql import raw_sql
from common.render import render
import simplejson


global_times_range = ['hours4','hours25','week1','month1','year1']


def get_rrdfiles_by_host(host):
    rrdfiles_list = list()
    host_dict = dict()
    host_perfdata_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),host)
    for root, dirs, files in os.walk(host_perfdata_path):
        for name in files:
            if name[-4:] == ".rrd":
                exists = 0
                for ranges in global_times_range:
                    if os.path.exists(os.path.join(os.path.dirname(os.path.abspath(__file__)), host, name[:-4] + '_' + ranges + '.png')):
                        exists +=1
                    if exists == len(global_times_range):
                        rrdfiles_list.append(name[:-4])
    host_dict[host] = rrdfiles_list
    return host_dict


def perfdata_host_service(request, host, service):
    if service == "all":
        perfdata_path = os.path.dirname(os.path.abspath(__file__))
        return render('perfdata/main.html', {'show_host_chart':True, 'host_dict':get_rrdfiles_by_host(host)}, request)
    else:
        return render('perfdata/main.html', {'show_service_chart':True, 'host_and_service':{host:service}}, request)


def get_chart(request, host, service, ranges):
    host_perfdata_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),host,service + '_' + ranges + '.png')
    if os.path.exists(host_perfdata_path):
        fd = open(host_perfdata_path, 'rb')
        image_content = fd.read()
        response = HttpResponse(image_content, mimetype="image/png")
        response['Cache-Control'] = 'no-cache'
        return response
    
