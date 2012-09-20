import simplejson
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from common.render import render
from common.decorators import require_permission
from tools.db import Instances, Session
from instances.models import Instances_Config


def format_ip_address(address):
    if address:
        ip_list = list()
        address = eval(address)
        try:
            (not address) and getattr(address,'private')
        except:
            return ip_list
        try:
            if not isinstance(address,dict):
                address = eval(address)
            for i in address['private']:
                if i:
                    ip_list.append(i['addr'])
                else:
                    ip_list.append(None)
        except TypeError,e:
            raise e
        return ip_list


def get_instances_list(ins):
    final_instances = list()
    for instance in ins:
        ins = dict()
        ins['physical_host'] = instance.physical_host
        ins['ip_address'] = format_ip_address(instance.ip_address)
        ins['uuid'] = instance.uuid
        ins['name'] = instance.name
        ins['state'] = instance.state
        ins['last_update_time'] = instance.last_update_time.strftime('%Y-%m-%d %H:%M')
        ins['moniting_state'] = instance.moniting_state if not instance.moniting_state else simplejson.loads(instance.moniting_state)
        ins['notification_state'] = instance.notification_state if not instance.notification_state else simplejson.loads(instance.notification_state)
        final_instances.append(ins)
    return final_instances


def get_instances_detail(ins):
    final_instances = list()
    for instance in ins:
        ins = dict()
        ins['physical_host'] = instance.physical_host
        ins['ip_address'] = format_ip_address(instance.ip_address)
        ins['uuid'] = instance.uuid
        ins['name'] = instance.name
        ins['state'] = instance.state
        ins['last_update_time'] = instance.last_update_time.strftime('%Y-%m-%d %H:%M')
        ins['moniting_state'] = instance.moniting_state if not instance.moniting_state else simplejson.loads(instance.moniting_state)
        ins['notification_state'] = instance.notification_state if not instance.notification_state else simplejson.loads(instance.notification_state)
        final_instances.append(ins)
    
    physical_host_list = list()
    for i in final_instances:
        host = i.__getitem__('physical_host')
        if host:
            physical_host_list.append(host)
    physical_host_list = list(set(physical_host_list))
    
    def get_host_instances(host):
        i = 0
        temp_list = list()
        for ins in final_instances:
            temp_dict = dict()
            if host == ins.__getitem__('physical_host'):
                temp_dict[i] = ins
                temp_list.append(temp_dict)
                i += 1
        return temp_list
    
    
    final_host_dict = dict()
    for host in physical_host_list:
        final_host_dict[host] = get_host_instances(host)
    return final_host_dict


@csrf_exempt
def get_instance_state(request):
    if request.method == "POST":
        post = request.POST
        uuid = eval(post['data'])
        session = Session()
        instance = session.query(Instances).filter_by(uuid=uuid).all()
        return HttpResponse(simplejson.dumps(get_instances_list(instance)))


def get_portlist(portlist):
    if not portlist: return None
    return portlist if not ',' in portlist else portlist.split(',')


def get_instances_config(instances):
    temp = dict()
    i = instances
    temp['name'] = i.name
    temp['uuid'] = i.uuid
    temp['moniting_state'] = i.moniting_state if not i.moniting_state else eval(i.moniting_state)
    temp['notification_state'] = i.notification_state if not i.notification_state else eval(i.notification_state)
    
    def format_tcp_port(portlist):
        if not isinstance(portlist,list): return portlist
        tcp = ""
        for p in portlist:
           p += ','
           tcp += p
        return tcp.rstrip(',')
    temp['moniting_state']['tcp'] = format_tcp_port(temp['moniting_state']['tcp'])
    
    def format_udp_port(portlist):
        if not isinstance(portlist,list): return portlist
        udp = ""
        for p in portlist:
           p += ','
           udp += p
        return udp.rstrip(',')
    temp['moniting_state']['udp'] = format_udp_port(temp['moniting_state']['udp'])
    
    return temp


@require_permission('Operator')
def instances_detail(request):
    session = Session()
    session.autoflush=True
    ins = session.query(Instances).all()
    final_instances = get_instances_detail(ins)
    return render('instances/instance_detail.html',{'instances':simplejson.dumps(final_instances)},request)


@require_permission('Operator')
def instances_list(request):
    session = Session()
    session.autoflush=True
    ins = session.query(Instances).all()
    final_instances = get_instances_list(ins)
    return render('instances/instance_list.html',{'instances':final_instances},request)


@require_permission('Admin')
def instances_setting(request,uuid):
    if request.method == "POST":
        data = request.POST
        try:
            arp = data['arp']
        except:
            arp = None
        try:
            ping = data['ping']
        except:
            ping = None
        tcp = data['tcp']
        udp = data['udp']
        name = data['instance_name']
        ip = data['instance_ip']
        moniting_data = dict()
        moniting_data['ping'] = True if ping =='on' else None
        moniting_data['arp'] = True if arp == 'on' else None
        moniting_data['tcp'] = get_portlist(tcp)
        moniting_data['udp'] = get_portlist(udp)
        
        notification_data = dict()
        notification_data['cpu_warnning'] = data['cpu_warnning'] if data['cpu_warnning'] else 0
        notification_data['cpu_critical'] = data['cpu_critical'] if data['cpu_critical'] else 0
        notification_data['disk_usage_warnning'] = data['disk_usage_warnning'] if data['disk_usage_warnning'] else 0
        notification_data['disk_usage_critical'] = data['disk_usage_critical'] if data['disk_usage_critical'] else 0
        notification_data['bandwidth_usage_warnning'] = data['bandwidth_usage_warnning'] if data['bandwidth_usage_warnning'] else 0
        notification_data['bandwidth_usage_critical'] = data['bandwidth_usage_critical'] if data['bandwidth_usage_critical'] else 0
        try:
            ins = Instances_Config.objects.get(uuid=uuid)
        except Exception,e:
            instances = Instances_Config(
                name = name,
                ipaddress = ip,
                uuid = uuid,
                notification_state = notification_data,
                moniting_state = moniting_data
            )
            instances.save()
        else:
            Instances_Config.objects.filter(uuid=uuid).update(
                notification_state = notification_data,
                moniting_state = moniting_data
            )
        return render('instances/notification.html',{'finish_update':True},request)
        
        
    uuid = uuid.strip()
    session = Session()
    instance = session.query(Instances).filter(Instances.uuid==uuid).all()
    final_instance = get_instances_list(instance)
    try:
        instance_config = Instances_Config.objects.get(uuid=uuid)
        final_instance_config = get_instances_config(instance_config)
    except:
        final_instance_config = None
    return render('instances/notification.html',{'instance_info':final_instance[0],'instance_config':final_instance_config},request)


@csrf_exempt
def instances_config(request):
    if request.method == "POST":
        instances_config = Instances_Config.objects.all().values()
        return HttpResponse(str(instances_config))
    return HttpResponse()
    