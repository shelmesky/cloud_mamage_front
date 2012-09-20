import datetime

from django.core.paginator import Paginator, InvalidPage, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.conf import settings

from log_logentries.models import Notification
from common.render import render
from common.decorators import require_permission
from users.models import Account

datetime_format = settings.DATETIME_FORMAT_CUSTOMIZE


@require_permission('Operator')
def advanced_search(request):
    return render('notification/search.html', {}, request)


@require_permission('Operator')
def advanced_search_result(request):
        data = request.GET
    
        keyword = data.get('keyword',None)
        critical = 2 if data.get('critical',None) else 0
        warning = 1 if data.get('warning',None) else 0
        unknown = 3 if data.get('unknown',None) else 0
        starttime = data.get('starttime',None)
        endtime = data.get('endtime',None)
        
        if starttime and endtime:
            start_time = datetime.datetime.strptime(starttime,datetime_format)
            end_time = datetime.datetime.strptime(endtime,datetime_format)
        else:
            start_time = end_time = None
        
        keyword = keyword.strip().lower()

        if start_time and end_time and keyword:
            notifications = Notification.objects.filter(Q(hostname__icontains=keyword) | Q(service_description__icontains=keyword) |
                                                        Q(output__icontains=keyword),
                                                        has_processed=None,
                                                        ).filter(
                                                        Q(created_time__gt=start_time) &
                                                        Q(created_time__lt=end_time)
                                                        )
        elif start_time and end_time:
            notifications = Notification.objects.filter(
                                                        Q(created_time__gt=start_time) &
                                                        Q(created_time__lt=end_time)
                                                        )
        elif keyword:
            notifications = Notification.objects.filter(Q(hostname__icontains=keyword) | Q(service_description__icontains=keyword) |
                                                        Q(output__icontains=keyword),
                                                        has_processed=None,
                                                        )
        else:
            notifications = None
        
        if notifications:
            if critical and not warning and not unknown:
                notifications = notifications.filter(Q(state__iexact=critical))
            elif warning and not critical and not unknown:
                notifications = notifications.filter(Q(state__iexact=warning))
            elif unknown and not critical and not warning:
                notifications = notifications.filter(Q(state__iexact=unknown))
            elif critical and warning and not unknown:
                notifications = notifications.filter(Q(state__iexact=critical) or Q(state__iexact=warning))
            elif critical and unknown and not warning:
                notifications = notifications.filter(Q(state__iexact=critical) or Q(state__iexact=unknown))
            elif warning and unknown and not critical:
                notifications = notifications.filter(Q(state__iexact=warning) or Q(state__iexact=unknown))
            elif critical and warning and unknown:
                notifications = notifications.filter(Q(state__iexact=warning) or Q(state__iexact=unknown) or Q(state__iexact=unknown))
        else:
            notifications = Notification.objects.filter(Q(state__iexact=warning) or Q(state__iexact=unknown) or Q(state__iexact=unknown))
        
        users = Account.objects.all()
        user_list = list()
        for user in users:
            user_list.append(user.username)
        
        page_size = 13
        after_range_num = 4
        before_range_num = 5
        try:
            page = int(request.GET.get('page',1))
            if page < 1:
                page = 1
        except ValueError:
            page = 1
        paginator = Paginator(notifications,page_size)
        try:
            paged_notifications = paginator.page(page)
        except(EmptyPage, InvalidPage, PageNotAnInteger):
            rulers = paginator.page(1)
        if page >= after_range_num:
            page_range = paginator.page_range[page - after_range_num : page + before_range_num]
        else:
            page_range = paginator.page_range[0:int(page) + before_range_num]   
        
        return render('notification/search_result.html',{'notifications':paged_notifications,
                                                         'original_notifications':notifications,
                                                         'user_list':user_list,
                                                         'keyword':keyword,
                                                         'starttime':start_time.strftime(datetime_format) if start_time else '',
                                                         'endtime':end_time.strftime(datetime_format) if end_time else '',
                                                         'critical':'on' if critical==2 else '',
                                                         'warning':'on' if warning==1 else '',
                                                         'unknown':'on' if unknown==3 else '',
                                                         },request)


@require_permission('Admin')
def show_notification(request):
    """
    view for notification and search form
    """
    keyword = request.REQUEST.get("keyword",None)
    
    users = Account.objects.all()
    user_list = list()
    for user in users:
        user_list.append(user.username)
        
    if keyword:
        keyword = keyword.strip().lower()
        if len(keyword) == 0:
            return render('notification/main.html',{'host_not_exist':True},request)
        
        if keyword.startswith('#'):
            keyword = keyword.split('#')[1]
            notifications = Notification.objects.filter(Q(id__iexact=keyword), has_processed=None)
        else:
            notifications = Notification.objects.filter(Q(hostname__icontains=keyword) | Q(service_description__icontains=keyword) |
                                                        Q(output__icontains=keyword) | Q(id__iexact=keyword), has_processed=None)
        if not notifications:
            return render('notification/main.html',{'host_not_exist':True},request)
        
        page_size = 13
        after_range_num = 4
        before_range_num = 5
        try:
            page = int(request.GET.get('page',1))
            if page < 1:
                page = 1
        except ValueError:
            page = 1
        paginator = Paginator(notifications,page_size)
        try:
            paged_notifications = paginator.page(page)
        except(EmptyPage, InvalidPage, PageNotAnInteger):
            rulers = paginator.page(1)
        if page >= after_range_num:
            page_range = paginator.page_range[page - after_range_num : page + before_range_num]
        else:
            page_range = paginator.page_range[0:int(page) + before_range_num]
        
        return render('notification/main.html',{'notifications':paged_notifications,'original_notifications':notifications, 'user_list':user_list, 'keyword':keyword},request)
    
    elif not keyword and request.REQUEST.get("source")=="form":
        return render('notification/main.html', {'empty_keyword':True}, request)
    
    else:
        notifications = Notification.objects.filter(has_processed=None)
        if not notifications:
            return render('notification/main.html',{'host_not_exist':True},request)
        
        page_size = 13
        after_range_num = 4
        before_range_num = 5
        try:
            page = int(request.GET.get('page',1))
            if page < 1:
                page = 1
        except ValueError:
            page = 1
        paginator = Paginator(notifications,page_size)
        try:
            paged_notifications = paginator.page(page)
        except(EmptyPage, InvalidPage, PageNotAnInteger):
            rulers = paginator.page(1)
        if page >= after_range_num:
            page_range = paginator.page_range[page - after_range_num : page + before_range_num]
        else:
            page_range = paginator.page_range[0:int(page) + before_range_num]
        
        return render('notification/main.html',{'notifications':paged_notifications,'original_notifications':notifications, 'user_list':user_list},request)

