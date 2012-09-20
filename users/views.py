from django import shortcuts
from django.http import HttpResponse
from django.contrib import messages
from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse

from common.render import render
from users.models import Account
from common.performe_raw_sql import raw_sql
from log_logentries.models import Notification
from process_notification.models import Notification_Result



def _set_session_data(request,account):
    request.session['username'] = account.username
    request.session['email'] = account.email
    request.session['group_name'] = account.get_group_name_display()
    request.session['last_login'] = account.last_login
    request.session['is_valid'] = account.is_valid
    request.session['date_joined'] = account.date_joined
    request.session['has_login'] = True


def login(request):
    if request.method == "POST":
        data = request.POST
        if not data:
            return render('users/login.html',{},request)
        username = data['username']
        password = data['password']
        try:
            account = Account.objects.get(username=username,password=password)
        except:
            messages.error(request,_('Invalid email or password.'))
            return render('users/login.html',{},request)
            
        if not account.is_valid:
            messages.error(request,_('Your account is locked, please contact to administrator.'))
            return render('users/login.html',{},request)
        
        
        _set_session_data(request,account)
        
        return shortcuts.redirect(reverse('home'))
    
    return render('users/login.html',{},request)


def logout(request):
    username = request.session['username']
    request.session.clear()
    if username:
        messages.success(request,_('%s logout successfully!') % username)
    
    return shortcuts.redirect(reverse('login'))


def signup(request):
    return HttpResponse('signup')


def home(request):
    hosts_sql = """
    SELECT COUNT( * ) AS quantity
    FROM nagios_hosts a, nagios_hoststatus b
    WHERE a.host_object_id = b.host_object_id
    AND a.instance_id = b.instance_id
    AND b.current_state !=0
    """
    hosts_cursor = raw_sql(hosts_sql)
    hosts_rows = hosts_cursor.fetchall()
    problem_hosts = int(hosts_rows[0][0])
    
    services_sql = """
    SELECT COUNT( * ) AS quantity
    FROM nagios_services a, nagios_servicestatus b
    WHERE a.service_object_id = b.service_object_id
    AND a.instance_id = b.instance_id
    AND b.current_state !=0
    """
    services_cursor = raw_sql(services_sql)
    services_rows = services_cursor.fetchall()
    problem_services = int(services_rows[0][0])
    
    notifications = Notification.objects.filter(has_processed=None)
    unhandled_notifications = len(notifications)
    
    jobs = Notification_Result.objects.filter(to_user=request.session.get('username',None),op_processed_result=None)
    unhandled_jobs = len(jobs)
    
    return render('users/home.html',{'problem_hosts':problem_hosts,
                                    'problem_services':problem_services,
                                    'unhandled_notifications':unhandled_notifications,
                                    'unhandled_jobs':unhandled_jobs
                                     },request)


def profile(request):
    if request.method == "POST":
        data = request.POST
        password = data.get('password',None)
        email = data.get('email',None)
        cell_phone = data.get('cell_phone',None)
        
        if password and email and cell_phone:
            try:
                user = Account.objects.get(username=request.session.get('username'))
            except Account.DoesNotExist:
                return render('users/profile.html',{'user_not_exist':True},request)
            else:
                Account.objects.filter(username=request.session.get('username')).update(
                    password=password.strip(),
                    email=email.strip(),
                    cell_phone=cell_phone.strip()
                )
                return render('users/profile.html',{'finished':True},request)
    try:
        user = Account.objects.get(username=request.session.get('username'))
    except Account.DoesNotExist:
        return render('users/profile.html',{'user_not_exist':True},request)
    
    return render('users/profile.html',{'user':user},request)

