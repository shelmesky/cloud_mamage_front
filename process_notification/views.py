#coding: utf-8
from hashlib import md5
import simplejson
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from process_notification.models import Notification_Result
from log_logentries.models import Notification
from common.decorators import require_permission

@csrf_exempt
@require_permission('Admin')
def update(request):
    if request.method == "POST":
        data = request.POST['data']
        data = eval(data)
        notification_id = data['id']
        processed_result = data['result']
        user = data['user']
        
        # make md5 signature for message
        noti_ori_message = Notification.objects.get(id=notification_id)
        md5_str = noti_ori_message.hostname + noti_ori_message.service_description + str(noti_ori_message.state)
        msg_md5 = md5(md5_str).hexdigest()
        
        from_user = request.session['username']
        to_user = user
        result = processed_result
        notification_id = notification_id
        message_md5 = msg_md5
        
        noti_processed = Notification_Result(
            from_user = from_user,
            to_user = to_user,
            result = result,
            notification_id = notification_id,
            message_md5 = message_md5
        )
        # set the original message has processed!
        Notification.objects.filter(id=notification_id).update(has_processed=1)
        noti_processed.save()
        
        return HttpResponse(simplejson.dumps({"message":"success"}))
    return HttpResponse()

@csrf_exempt
@require_permission('Admin')
def revoke(request):
    if request.method == "POST":
        try:
            noti_id = request.POST['data']
            Notification.objects.get(id=noti_id).delete()
        except Exception,e:
            raise e
        return HttpResponse(simplejson.dumps({'message':'success'}))
    return HttpResponse()

