import datetime
import threading
from django import template

from system.models import SendRuler
from users.models import Account
from common.api.cloudmessage.sms import WangXinTongSmsClient


def notification_body(hostname, state, service_description, output):
    context = {
        'datetime':datetime.datetime.now().strftime('%Y-%m-%d %H:%M'),
        'hostname':hostname,
        'state':state,
        'service_description':service_description,
        'output':output
    }
    return template.loader.render_to_string('utils/notification_plain.html',context)


class RulerSender(threading.Thread):
    def __init__(self,message):
        super(RulerSender,self).__init__()
        self.message = message
        self.daemon = True

    def run(self):
        try:
            rulers = SendRuler.objects.all()
        except SendRuler.DoesNotExist:
            return
        
        hostname = self.message.get('hostname',None)
        state = self.message.get('state',None)
        service_description = self.message.get('service_description',None)
        output = self.message.get('output',None)
        
        not_empty_rulers = list()
        
        for rule in rulers:
            temp = dict()
            temp['username'] = rule.user_name
            if len(eval(rule.host_name)) != 0:
                temp['hostname'] = eval(rule.host_name)
            if rule.host_name_include:
                temp['hostname_include'] = rule.host_name_include
            if len(eval(rule.state)) != 0:
                temp['state'] = eval(rule.state)
            if rule.output:
                temp['output'] = rule.output
            not_empty_rulers.append(temp)
        
        
        for rule in not_empty_rulers:
            total_effctive_rulers = len(rule)-1
            effctive_rulers = 0
            for key,value in rule.items():
                if key != 'username':
                    if key == 'hostname':
                        for host in value:
                            if host in hostname:
                                effctive_rulers += 1
                    
                    if key == 'state':
                        for stat in value:
                            if stat in state:
                                effctive_rulers += 1
                    
                    if key == 'hostname_include':
                        if value in hostname:
                            effctive_rulers += 1
                    
                    if key == "output":
                        if value in output:
                            effctive_rulers += 1
            
            # if we got matched ruler, send message to ruler's username, and exit ruler table.
            if effctive_rulers == total_effctive_rulers:
                username = eval(rule.get('username',None))[0]
                cell_phone = Account.objects.get(username=username).cell_phone
                message_body = notification_body(hostname,state[0],service_description,output)
                sms_client = WangXinTongSmsClient()
                sms_client.send_sms(cell_phone, message_body)
                return


def RulerProcesser(message):
    ruler_sender = RulerSender(message)
    ruler_sender.start()
    ruler_sender.join()


