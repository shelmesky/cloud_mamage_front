import simplejson
import json
from django.http import HttpResponse
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator, InvalidPage, EmptyPage, PageNotAnInteger

from system.models import SendRuler
from common.render import render
from common.performe_raw_sql import raw_sql


def get_user_list():
    """
    get user list from nagios database by raw sql.
    """
    sql = """
    SELECT username
    FROM users_account
    """
    arr = list()
    cursor = raw_sql(sql)
    rows = cursor.fetchall()
    for row in rows:
        arr.append(row[0])
    return arr


def get_host_list():
    """
    get host list from nagios database by raw sql.
    """
    sql = """
    SELECT host_object_id, display_name
    FROM nagios_hosts;
    """
    arr = list()
    cursor = raw_sql(sql)
    rows = cursor.fetchall()
    for row in rows:
            arr.append(row)
    return arr


def get_host_service_list():
    """
    get service list from nagios database by raw sql.
    """
    arr = list()
    hosts_list = get_host_list()
    for k,v in hosts_list:
        temp = dict()
        temp[v] = list()
        sql = """
        SELECT display_name
        FROM nagios_services
        WHERE host_object_id=%s
        """ % k
        cursor = raw_sql(sql)
        rows = cursor.fetchall()
        for row in rows:
            temp[v].append(row[0])
        arr.append(temp)
    return arr

host_service_list = get_host_service_list()


def show_settings(request):
    """
    main view for display settings page.
    """
    all_ruler = SendRuler.objects.all()
    
    page_size = 6
    after_range_num = 4
    before_range_num = 5
    try:
        page = int(request.GET.get('page',1))
        if page < 1:
            page = 1
    except ValueError:
        page = 1
    paginator = Paginator(all_ruler,page_size)
    try:
        rulers = paginator.page(page)
    except(EmptyPage, InvalidPage, PageNotAnInteger):
        rulers = paginator.page(1)
    if page >= after_range_num:
        page_range = paginator.page_range[page - after_range_num : page + before_range_num]
    else:
        page_range = paginator.page_range[0:int(page) + before_range_num]
    
    final_rulers = list()
    
    for rule in rulers:
        temp = dict()
        temp['id'] = rule.id
        temp['created_time'] = rule.created_time
        temp['host_name'] = eval(rule.host_name)
        temp['host_name_include'] = rule.host_name_include
        temp['state'] = eval(rule.state)
        temp['user_name'] = eval(rule.user_name)
        temp['output'] = rule.output
        final_rulers.append(temp)
    
    return render('system/main.html',{'host_service_list':host_service_list,'users':get_user_list(), \
                                      'page_range':page_range, 'paged_ruler':rulers, 'original_ruler':final_rulers,\
                                        'host_service_list_json':json.dumps(host_service_list)}, request)


def update_settings(request):
    """
    update function used for settings page.
    """
    if request.method == "POST":
        data = request.POST
        host_list = data.getlist('host_list')
        host_list_include = data['host_list_include']
        state = data.getlist('state')
        user_list = data.getlist('user_list')
        output = data['output']
        state = data.getlist('state')
        p = SendRuler(
            host_name = host_list,
            host_name_include = host_list_include,
            user_name = user_list,
            state = state,
            output = output
        )
        p.save()    
        return render('system/main.html',{'updated':True},request)


@csrf_exempt
def get_ruler_list(request):
    if request.method == "GET":
        rulers = SendRuler.objects.all()
        rulers_list = list()
        for rule in rulers:
            rulers_list.append({'hostname':rule.host_name, 'hostname_inlcude':rule.host_name_include,
                                'state':rule.state, 'output':rule.output, 'username':rule.user_name})
        return HttpResponse(rulers_list)
