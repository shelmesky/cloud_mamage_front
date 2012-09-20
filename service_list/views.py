# Create your views here.
import time
from django.http import HttpResponse
from common.performe_raw_sql import raw_sql
from common.render import render


def service_list(request):
    host = request.REQUEST.get('host',None)
    service_type = request.REQUEST.get('service_type',None)
    
    if host:
        sql = """
        SELECT host_object_id
        FROM nagios_hosts
        WHERE display_name =  '%s'
        """ % host
        cursor = raw_sql(sql)
        rows = cursor.fetchall()
        try:
            host_object_id = rows[0][0]
        except:
            return render('service_list/main.html',{'host_not_exist':True},request)
        
        sql = """
        SELECT 
        a.host_object_id, a.service_object_id, a.display_name,
        (select now()) as status_update_time,b.last_state_change,b.current_state,b.output
        FROM nagios_services a, nagios_servicestatus b
        WHERE a.service_object_id = b.service_object_id
        AND a.instance_id = b.instance_id
        AND a.host_object_id = %d
        ORDER BY a.host_object_id,a.display_name ASC
        """ % host_object_id
        cursor = raw_sql(sql)
        rows = cursor.fetchall()
    else:
        if not service_type:
            sql = """
            SELECT
            a.host_object_id, a.service_object_id, a.display_name,
            (select now()) as status_update_time,b.last_state_change,b.current_state,b.output
            FROM nagios_services a, nagios_servicestatus b
            WHERE a.service_object_id = b.service_object_id
            AND a.instance_id = b.instance_id
            ORDER BY a.host_object_id,a.display_name ASC
            """
            cursor = raw_sql(sql)
            rows = cursor.fetchall()
        elif service_type == "unhandled":
            sql = """
            SELECT
            a.host_object_id, a.service_object_id, a.display_name,
            (select now()) as status_update_time,b.last_state_change,b.current_state,b.output
            FROM nagios_services a, nagios_servicestatus b
            WHERE a.service_object_id = b.service_object_id
            AND a.instance_id = b.instance_id
            AND b.current_state !=0
            ORDER BY a.host_object_id,a.display_name ASC
            """
            cursor = raw_sql(sql)
            rows = cursor.fetchall()
            
    ############### get unique host list ################
    sql = """
        SELECT host_object_id,display_name
        FROM nagios_hosts
        """
    cursor = raw_sql(sql)
    rows_temp = cursor.fetchall()
    unique_hostname_list = list()
    for line in rows_temp:
        unique_hostname_list.append({line[0]:line[1]})
    def get_hostname_from_id(host_id):
        for item in unique_hostname_list:
            for k,v in item.items():
                if host_id ==k:
                    return v
    ################## end get unique host list############
    
    service_list = list()
    for line in rows:
        temp = dict()
        temp['hostname'] = get_hostname_from_id(line[0])
        temp['host_object_id'] = line[0]
        temp['service_object_id'] = line[1]
        temp['display_name'] = line[2]
        duration = line[3] - line[4]
        hms = time.gmtime(duration.seconds)
        temp['state_duration'] = str(duration.days) + ' d ' + str(hms.tm_hour) + ' h ' + str(hms.tm_min) +  ' m ' + str(hms.tm_sec) + ' s'
        temp['current_state'] = line[5]
        temp['output'] = line[6]
        service_list.append(temp)
    return render('service_list/main.html',{'hostname_list':unique_hostname_list,'service_list':service_list},request)

