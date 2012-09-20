# Create your views here.
from django.http import HttpResponse
import uuid
import simplejson
from server import Admin_Receiver_Thread


def gen_message_id():
    return uuid.uuid4().get_hex()

def send_message(request):
    message = request.REQUEST.get('message',None)
    msg_id = gen_message_id()
    imessage = {
            'message_id':msg_id,
            'message_type':'add_host',
            'args':message
        }
    Admin_Receiver_Thread.send(simplejson.dumps(imessage))
    ret = Admin_Receiver_Thread.get_return(msg_id)
    return HttpResponse(simplejson.dumps(ret))