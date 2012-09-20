import simplejson
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from common.render import render
from common.decorators import require_permission
from process_notification.models import Notification_Result
from log_logentries.models import Notification


@require_permission('Operator')
def owner_job(request):
    """
    list jobs for current user.
    """
    final_dict = dict()
    noti_result_list = Notification_Result.objects.filter(to_user=request.session['username'],op_processed_result=None)
    if not noti_result_list:
        return render('jobs/owner_job.html',{'host_not_exist':True},request)
    for line in noti_result_list:
        final_dict[line.id] = {}
        final_dict[line.id]['notification'] = Notification.objects.get(id=line.notification_id)
        final_dict[line.id]['result'] = line
    generator_dict = [{key:final_dict[key]} for key in sorted(final_dict.keys(),reverse=True)]
    return render('jobs/owner_job.html',{'result_list':generator_dict},request)


@require_permission('Admin')
def dispatched_job(request):
    """
    list dispatched jobs for current user.
    """
    final_dict = dict()
    user = request.session['username']
    noti_result_list = Notification_Result.objects.filter(from_user=user)
    if not noti_result_list:
        return render('jobs/dispatched_job.html',{'host_not_exist':True},request)
    for line in noti_result_list:
        final_dict[line.id] = {}
        final_dict[line.id]['notification'] = Notification.objects.get(id=line.notification_id)
        final_dict[line.id]['result'] = line
    generator_dict = [{key:final_dict[key]} for key in sorted(final_dict.keys(),reverse=True)]
    return render('jobs/dispatched_job.html',{'result_list':generator_dict},request)


@csrf_exempt
def update_result(request):
    if request.method == "POST":
        data = eval(request.POST['data'])
        try:
            result_id = data['id']
            result_content = data['result']
        except Exception,e:
            raise e
        Notification_Result.objects.filter(id=result_id).update(op_processed_result=result_content)
        return HttpResponse(simplejson.dumps({'message':'success'}))
    return HttpResponse()

