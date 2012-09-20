import decimal
from django import template

register = template.Library()

@register.inclusion_tag('tag/show_instances_healthy.html', takes_context=False)
def render_instances_healthy_percent(moniting_state, notification_state, instance_state):
    # if instance has been shutdown, return 0 directly.
    if instance_state == "SHUTOFF":
        return {'percent':0}
    total_item = 0
    success_item = 0
    if moniting_state != None:
        items = ['arp','ping','tcp','udp']
        for k,v in moniting_state.items():
            if k not in 'uuid':
                for item in items:
                    try:
                        sub_item = v.__getitem__(item)
                    except Exception,e:
                        pass
                    else:
                        if sub_item == 1:
                            success_item += 1
                        total_item += 1
                        # total_item -= 1 : it means sub_item is a dict, so we will reduce 1 from total_item
                        if isinstance(sub_item,dict):
                            total_item -= 1
                            for port,result in sub_item.items():
                                if result == 1:
                                    success_item += 1
                                total_item += 1
                    
    if notification_state != None:
        for k,v in notification_state.items():
            if not k in ('cpu_usage_real','ip','uuid'):
                if v == 0:
                    success_item += 1
                total_item += 1
            
    if success_item and total_item:
        if success_item == 0:
            return {'percent':0}
        else:
            percent = int(decimal.Decimal(success_item)/decimal.Decimal(total_item)*100)
            return {'percent':percent}
    else:
        return {'percent':1}


@register.inclusion_tag('tag/show_hosts_healthy.html', takes_context=False)
def render_hosts_healthy_percent(host_object_id, hosts_state_list):
    host_list = list()
    for item in hosts_state_list:
        host_list.append(item[0])
    unique_host_list = list(set(host_list))
    
    host_list_dict = dict().fromkeys(unique_host_list,None)
    
    
    def get_total_and_success(id):
        total_item = 0
        success_item = 0
        for i in hosts_state_list:
            if i[0] == id:
                if i[1] == 0:
                    success_item += 1
                total_item += 1
        return total_item,success_item
    
    
    for host_id in unique_host_list:
        total_item,success_item = get_total_and_success(host_id)
        host_list_dict[host_id] =  int(decimal.Decimal(success_item)/decimal.Decimal(total_item)*100)
    
    percent = {'percent':host_list_dict.__getitem__(host_object_id)}
    return percent



