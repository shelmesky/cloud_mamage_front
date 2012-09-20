#coding=utf-8
#!/usr/bin/python
import sys
import os
import imp
import time
import Queue
import threading

PARENT_PATH = os.path.dirname(os.getcwd())
sys.path.insert(0, PARENT_PATH)

# we can use django's mod from outside django
# so this file will run in console mod
from django.core.management import setup_environ
import settings
setup_environ(settings)

from django.template import Template, Context

from common.performe_raw_sql import raw_sql
from common.monitor import ThreadPoolMonitor

RRD_TOOL = settings.RRD_TOOL
global_times_range = ['hours4','hours25','week1','month1','year1']



def get_hosts_list():
    sql = "select display_name from nagios_hosts"
    cursor = raw_sql(sql)
    rows = cursor.fetchall()
    ret_list = list()
    for row in rows:
        ret_list.append(row[0])
    return ret_list

def get_rrdfiles():
    rrdfiles_list = list()
    for host in get_hosts_list():
        host_rrdfile_path = os.path.join(PARENT_PATH, 'perfdata', host)
        for root, dirs, files in os.walk(host_rrdfile_path):
            for name in files:
                if name[-4:] == ".rrd":
                    rrdfiles_list.append(os.path.join(root,name))
    return rrdfiles_list


def import_from_file(module_path, package):
    if os.path.exists(module_path):
        f,filename,desc = imp.find_module(package,[module_path])
        loader = imp.load_module(package, f, filename, desc)
        return loader


class MakeRrds(threading.Thread):
    def __init__(self, rrds_queue):
        super(MakeRrds,self).__init__()
        self.daemon = False
        self.rrds_queue = rrds_queue
        
    def run(self):
        while 1:
            for rrd_file in get_rrdfiles():
                self.rrds_queue.put(rrd_file)
            time.sleep(60)


class MakeGraph(threading.Thread):
    def __init__(self, rrds_queue):
        super(MakeGraph,self).__init__()
        self.daemon = False
        self.rrds_queue = rrds_queue
        
    def run(self):
        while 1:
            rrd_file_absolute = self.rrds_queue.get()
            except_suffix_name = os.path.basename(rrd_file_absolute)[:-4]
            template_dir = os.path.join(os.path.dirname(rrd_file_absolute),"templates")
            if os.path.exists(template_dir):
                loader = import_from_file(template_dir, except_suffix_name)
                time_ranges = global_times_range
                for ranges in time_ranges:
                    origin_command = (loader.__dict__.get(ranges, None))
                    if origin_command:
                        template = Template(origin_command)
                        context = Context({'rrd_file':rrd_file_absolute})
                        command = template.render(context)
                        png_path = os.path.join(os.path.dirname(rrd_file_absolute), except_suffix_name + '_' + ranges + '.png')
                        png_path = png_path.encode('utf-8')
                        os.system(RRD_TOOL + " graph " + png_path + ' \\' + command.encode('utf-8'))
                    loader.__dict__.__setitem__(ranges, None)
            else:
                pass


def RunMakeGraph():
    rrds_queue = Queue.Queue()
    
    make_rrds_pool = []
    for i in range(1):
        make_rrds_pool.append(MakeRrds(rrds_queue))
    for i in make_rrds_pool:
        i.start()
    
    
    make_graph_pool = []
    for i in range(300):
        make_graph_pool.append(MakeGraph(rrds_queue))
    for i in make_graph_pool:
        i.start()
    
    
    monitor = ThreadPoolMonitor(make_rrds_pool=(make_rrds_pool, rrds_queue), \
                      make_graph_pool=(make_graph_pool, rrds_queue))
    monitor.start()


if __name__ == '__main__':
    RunMakeGraph()
    