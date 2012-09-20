from django.conf import settings

from common.api import httpclient
from common.api import exceptions


class WangXinTongSmsClient(object):
    '''
    APIs documented at: http://www.ldsms.com/SmsService.asmx
    Not accept json as request params, and only return response in html/xml.
    '''
    
    SERVER_ENCODING = 'GBK'  # WangXintong only accept GBK  :(
    
    def __init__(self, username=settings.WANG_XIN_TONG_USERNAME,
             password=settings.WANG_XIN_TONG_PASSWORD, url=settings.WANG_XIN_TONG_SERVICE_URL):
        
        self.username = username
        self.password = password
        self.url = url
        self.client = httpclient.HTTPClient(accept='application/xml', # only return xml 
                                            content_type='application/x-www-form-urlencoded') # donot accept json
        
    def _check_result(self, body):
        return_code = body.text
        if return_code == '-1':
            raise exceptions.Unauthorized(403, message='Authorization failed for WangXinTong service.')
        if return_code == '-2':
            raise exceptions.BadRequest(404, message='The length of message content is too large.')
        if return_code == '-3':
            raise exceptions.BadRequest(404, message='The message contains invalid/illegal words.')
        if return_code == '-4':
            raise exceptions.OverLimit(413, message='Your WangXinTong account [%s] if out of balance.' % self.username)
        if return_code == '-5':
            raise exceptions.BadRequest(404, message='Wrong match for cellphone number and parameters.')
        if return_code == '-1001':
            raise exceptions.SeverError(500, message='Server error on WangXinTong.')
    
    
    def _get(self, action):
        _url = '%s?username=%s&password=%s' % (action, self.username, self.password)
        resp, body = self.client.get(self.url + _url)
        self._check_result(body)
        return body
    
        
    def _post(self, action, params={}):
        body = {'username':self.username, 'password':self.password}
        body.update(params)
        resp, body = self.client.post(self.url+action, body=body)
        self._check_result(body)
        return body
    
    
    def get_balance(self):
        return self._get('GetBalance').text
    
    
    def send_sms(self, receivers, content):
        '''
        Receivers split by comma, eg: 13712341234,13812341234,13912341234
        '''
        try:
            content = content.encode(self.SERVER_ENCODING)  # prepare for urlencode
        except:
            pass
        
        return self._post('SendSMS', {'mobile':receivers, 'smscontent':content})
