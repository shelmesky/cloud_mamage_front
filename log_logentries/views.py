#coding: utf-8
import simplejson
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from log_logentries.models import Notification
from process_notification.models import Notification_Result
from common.performe_raw_sql import raw_sql
from common.ruler_sender import RulerProcesser

from common import LOG


@csrf_exempt
def receive_notification(request):
    """
    receive notification from remove monitor client.
    """
    if request.method == "POST":
        data = request.POST
        hostname = data['host_name']
        state = data['state']
        notification_type = data['notification_type']
        msg_type = data['type']
        output = data['output']
        service_description = data['service_description']
        message_from = data.get('from',None)
        if message_from == 'nagios':
            RulerProcesser(
                {'hostname':hostname,
                'state':state,
                'output':output,
                'service_description':service_description
                }
            )
        notification = Notification(
            hostname = hostname,
            state = int(state),
            service_description = service_description,
            notification_type = int(notification_type),
            output = output,
            msg_type = msg_type
        )
        notification.save()
        return HttpResponse(simplejson.dumps({"message":"success"}))
    return HttpResponse()


@csrf_exempt
def check_md5(request):
    """
    check md5 for notification.
    """
    if request.method == "POST":
        md5 = request.POST['data']
        noti_result = Notification_Result.objects.filter(message_md5=md5)
        # if can't get any recorder, noti_result will be a empty list.
        if not noti_result:
            return HttpResponse(0)
        for line in noti_result:
            if not line.op_processed_result:
                return HttpResponse(1)
        return HttpResponse(0)
    return HttpResponse()
