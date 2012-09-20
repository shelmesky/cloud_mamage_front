from django.core.urlresolvers import reverse
from django.contrib import messages
from django.utils.translation import ugettext as _
from django import shortcuts


class CloudManageLoginMiddleware(object):
    def process_view(self,request,view_func,view_args,view_kwargs):
        """
        check login status for user in specify urls.
        if not login, redirect to login page.
        """
        urls = ['home','host_list','service_list','notifications','advanced_search','system_settings','process_notification','revoke_notification', \
                'instances-list','instances-detail', 'owner_job','dispatched_job']
        
        for url in urls:
            if request.path == reverse(url):
                try:
                    request.session['has_login']
                except:
                    messages.error(request, _('Please login before this operation.'))
                    return shortcuts.redirect(reverse('login'))