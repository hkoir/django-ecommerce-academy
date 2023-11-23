# visitors/views.py

from django.shortcuts import render
from visitors.models import VisitorLog
from django.db.models import Count, Max
from django.db.models import Q



# def visitor_log(request):
#     visitors = VisitorLog.objects.values('user_name', 'session_key','ip_address','timestamp') \
#         .annotate(total_visits=Count('id')) \
#         .order_by('user_name', 'session_key','ip_address','timestamp')

#     return render(request, 'visitors/visitor_log.html', {'visitors': visitors})

def visitor_log(request):
    visitors = VisitorLog.objects.values('user_name', 'session_key', 'ip_address') \
        .annotate(total_visits=Count('id'), latest_timestamp=Max('timestamp')) \
        .order_by('user_name', 'session_key', 'ip_address')

    return render(request, 'visitors/visitor_log.html', {'visitors': visitors})