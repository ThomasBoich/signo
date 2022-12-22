from datetime import date, timedelta, datetime

from django.utils import timezone
from django.utils.timezone import make_aware
from django.db.models import Q

from documents.models import Document


def get_dates(period, all_documents):
    today = datetime.now()
    if period == '7':
        start_date = today - timedelta(days=7)
        end_date = today
    elif period == '30':
        start_date = today.replace(day=1)
        end_date = today
    elif period == '60':
        this_start = today.replace(day=1)
        end_date = this_start - timedelta(days=1)
        start_date = end_date.replace(day=1)
    elif period == 'all':
        start_date = all_documents.last().send_date
        end_date = today
    elif '+' in period:
        start_date = datetime(year=int(period[0:4]), month=int(period[5:7]), day=int(period[8:10]))
        end_date = datetime(year=int(period[11:15]), month=int(period[16:18]), day=int(period[19:21]))

    if start_date.tzinfo is None or \
        start_date.tzinfo.utcoffset(start_date) is None:
        
        tz = timezone.get_current_timezone()
        start_date = make_aware(start_date, tz, True)

    return start_date, end_date


def filter_by_name(search_name):
    if search_name:
        all_documents = Document.objects.filter(
            Q(sender__first_name__icontains=search_name)|
            Q(sender__last_name__icontains=search_name)|
            Q(recipient__first_name__icontains=search_name)|
            Q(recipient__last_name__icontains=search_name)
            ).order_by('-send_date')
    else:
        all_documents = Document.objects.all().order_by('-send_date')

    return all_documents