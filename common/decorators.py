from django.contrib import messages
from django.utils.translation import ugettext as _
from django import shortcuts
from django.core.urlresolvers import reverse
from users.conf.settings import G


def require_permission(access_group):
    """
    decorator for views used to check user's permission.
    """
    def wrap(func):
        def wrapper(request,*args,**kwargs):
            group_name = request.session['group_name']
            if G(group_name) >= G(access_group):
                return func(request,*args,**kwargs)
            else:
                messages.error(request, _('You do not have this permissions.'))
                return shortcuts.redirect(reverse('home'))
        return wrapper
    return wrap