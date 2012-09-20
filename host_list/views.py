# Create your views here.
import time
import simplejson
from django.http import HttpResponse
from common.performe_raw_sql import raw_sql
from common.render import render


def get_hosts_state():
    sql = """
    SELECT a.host_object_id, b.current_state
    FROM nagios_services a, nagios_servicestatus b
    WHERE a.service_object_id = b.service_object_id
    AND a.instance_id = b.instance_id
    ORDER BY a.host_object_id, a.display_name ASC 
    """
    cursor = raw_sql(sql)
    rows = cursor.fetchall()
    return rows

def host_list(request):
    host_type = request.REQUEST.get('host_type',None)
    if not host_type:
        sql = """
        SELECT
        a.host_object_id,a.display_name,a.address,
        b.current_state,(select now()) as status_update_time,b.last_state_change,b.output
        FROM nagios_hosts a, nagios_hoststatus b
        WHERE a.host_object_id = b.host_object_id AND a.instance_id = b.instance_id
        ORDER by a.display_name ASC
        """
    elif host_type == "unhandled":
        sql = """
        SELECT
        a.host_object_id,a.display_name,a.address,
        b.current_state,(select now()) as status_update_time,b.last_state_change,b.output
        FROM nagios_hosts a, nagios_hoststatus b
        WHERE a.host_object_id = b.host_object_id AND a.instance_id = b.instance_id
        AND b.current_state !=0
        ORDER by a.display_name ASC
        """
    
    cursor = raw_sql(sql)
    rows = cursor.fetchall()
    host_list = list()
    for line in rows:
        temp = dict()
        temp['host_object_id'] = line[0]
        temp['display_name'] = line[1]
        temp['address'] = line[2]
        temp['current_state'] = line[3]
        duration = line[4] - line[5]
        hms = time.gmtime(duration.seconds)
        temp['state_duration'] = str(duration.days) + ' d ' + \
            str(hms.tm_hour) + ' h ' + str(hms.tm_min) +  ' m ' + str(hms.tm_sec) + ' s'
        temp['output'] = line[6]
        host_list.append(temp)
    return render('host_list/main.html',{'host_list':host_list,'services_list':get_hosts_state()},request)

