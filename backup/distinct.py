    #distinct_services = Notification.objects.exclude(service_description='(null)').values_list('service_description').distinct().order_by()
    #distinct_hosts = Notification.objects.values_list('hostname').distinct().order_by()
    #raise NameError,distinct_hosts