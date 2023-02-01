from datetime import date, timedelta, datetime
from reportlab.pdfgen import canvas
from unidecode import unidecode

from django.utils import timezone
from django.utils.timezone import make_aware
from django.db.models import Q
from django.conf import settings


from documents.models import Document

from .models import Action


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
    elif period == '':
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



def filter_all_documents(request, all_documents):
    
    search_name = request.GET.get('search')
    period = request.GET.get('period')
    
    # getting doc_type
    try:
        doc_type = request.GET.get('doc_type').upper()
    except:
        doc_type = ''

    # getting signed status
    try:
        signed = request.GET.get('signed').split('-')
    except:
        signed = ['']

    all_documents = filter_by_name(all_documents, search_name)
    if period:
        start_date, end_date = get_dates(period, all_documents) 
        all_documents = all_documents.filter(send_date__range=[start_date, end_date])

    if signed != ['']:
        signer = signed[0].upper()
        signed_status = signed[1].title()
        if signer in ['AD', 'DO']:
            all_documents = all_documents.filter(sender__type__in=[signer, 'DI'], sender_status=signed_status)
        elif signer == 'CL':
            all_documents = all_documents.filter(recipient__type=signer, recipient_status=signed_status)
        elif signer == "BOTH":
            all_documents = all_documents.filter(recipient__type='CL', 
                                                recipient_status=signed_status,
                                                sender__type__in=['AD', 'DO', 'DI'],
                                                sender_status=signed_status)

    if doc_type:
        all_documents = all_documents.filter(type__type_document=doc_type)

    sort_filter = request.GET.get('sort')
    if sort_filter:
        all_documents = all_documents.order_by(sort_filter)

    return all_documents



def filter_by_name(all_documents, search_name):
    if search_name and len(search_name.split(' ')) == 1:
        all_documents = all_documents.filter(
            Q(sender__first_name__icontains=search_name)|
            Q(sender__last_name__icontains=search_name)|
            Q(recipient__first_name__icontains=search_name)|
            Q(recipient__last_name__icontains=search_name)
            ).order_by('-send_date')
    elif search_name and len(search_name.split(' ')) == 2:
        name1 = search_name.split(' ')[0]
        name2 = search_name.split(' ')[1]
        all_documents = all_documents.filter(
            (Q(sender__first_name__icontains=name1) & Q(sender__last_name__icontains=name2)) |
            (Q(sender__first_name__icontains=name2) & Q(sender__last_name__icontains=name1)) |
            (Q(recipient__first_name__icontains=name1) & Q(recipient__last_name__icontains=name2)) |
            (Q(recipient__last_name__icontains=name2) & Q(recipient__last_name__icontains=name1))
        )
    else:
        all_documents = all_documents.order_by('-send_date')

    return all_documents



def filter_actions(request, actions):
    search_name = request.GET.get('search') or ''
    period = request.GET.get('period')

    actions = Action.objects.filter(action__icontains=search_name)
    if period:
        start_date, end_date = get_dates(period, actions) 
        actions = actions.filter(pub_date__range=[start_date, end_date])

    sort_filter = request.GET.get('sort')
    if sort_filter:
        all_documents = all_documents.order_by(sort_filter)

    return actions




from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

def create_signature(request, document):
    p = canvas.Canvas(settings.MEDIA_ROOT + '/signature.pdf')
    pdfmetrics.registerFont(TTFont('Arial', 'Arial.ttf'))
    p.setFont('Arial', 14)
    if request.user.type in ['AD', 'DO']:
        signature = f'{document.sender.last_name} {document.sender.first_name} {document.sender.patronymic} - подписал документ'
    elif request.user.type == 'CL':
        signature = f'{document.recipient.last_name} {document.recipient.first_name} {document.recipient.patronymic} - подписал документ'
    p.setFillColorRGB(0,0,1)
    p.drawString(40, 15, signature)
    
    p.showPage()
    p.save()
    







