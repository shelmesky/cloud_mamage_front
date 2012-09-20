from django.template import RequestContext
from django.shortcuts import render_to_response

def render(template_name,data=None,request=None):
    return render_to_response(template_name, data, context_instance=RequestContext(request))