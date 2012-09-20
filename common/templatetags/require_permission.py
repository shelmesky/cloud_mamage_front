from django import template
from users.conf.settings import G

register = template.Library()

class Check_Permission(template.Node):
    def __init__(self,nodelist,access_group):
        self.nodelist = nodelist
        self.access_group = access_group
    
    def render(self,context):
        access_group = self.access_group.resolve(context,True)
        request = context['request']
        output = self.nodelist.render(context)
        
        if G(request.session['group_name']) >= G(access_group):
            return output
        else:
            return ""

@register.tag(name='checkpermission')
def check_permission(parser,token):
    try:
        tag_name, access_group = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError, \
        "%r tag requires exactly one argument: args" % \
        token.split_contents[0]
    
    nodelist = parser.parse(('endcheckpermission',))
    parser.delete_first_token()
    access_group = parser.compile_filter(access_group)
    return Check_Permission(nodelist,access_group)
    