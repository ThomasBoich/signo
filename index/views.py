from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, redirect
# Create your views here.
from documents.models import Document, DocumentType
from users.models import CustomUser


@login_required
def index(request):
    ''' ГЛАВНАЯ СТРАНИЦА С ИНФОГРАФИКОЙ '''
    if request.user.is_authenticated == False:
        return redirect('login')
    # else:
        # all_documents_type = DocumentType.objects.all().count()
        
    # СТРАНИЦА АДМИНИСТРАТОРА
    if request.user.is_authenticated and request.user.type == 'AD':
        context = {
            'title': 'Главная страница',
            'all_users': CustomUser.objects.all().count(), # кол-во пользователей
            'all_doctors': CustomUser.objects.filter(type='DO').count(), # кол-во врачей
            'all_clients': CustomUser.objects.filter(type='CL').count(), # кол-во клиентов
            'all_active_documents': Document.objects.filter(
                Q(sender=request.user) | Q(recipient=request.user)).filter(
                    Q(sender_status=False) | Q(recipient_status=False)), # необработанные документы
            'type': DocumentType.objects.all(), # все типы документов
            'all_documents': Document.objects.all().count(), # кол-во документов
            'finish': Document.objects.all().filter(Q(sender_status=True) & Q(recipient_status=True)).count(), # кол-во подписанных документов
            'contract': Document.objects.filter(type__type_document='DOGOVOR').count(), # кол-во договоров
            'ids': Document.objects.filter(type__type_document='IDS').count(), # кол-во ИДС
            'medcard': Document.objects.filter(type__type_document='MEDCARD').count(), # кол-во медкард
            'admcard': Document.objects.filter(type__type_document='ADMCARD').count(), # кол-во адмкард
            'rent': Document.objects.filter(type__type_document='RENT').count(), # кол-во справок в налоговую
            'plan': Document.objects.filter(type__type_document='PLAN').count(), # кол-во планов лечения
            'medcarddne': Document.objects.filter(type__type_document='DNEVNIK').count(),
            'u': u,
        }
        return render(request, 'index/cabinet/ad.html', context)
    
    # СТРАНИЦА СУПЕРАДМИНИСТРАТОРА
    if request.user.is_authenticated and request.user.type == 'DI':
        g = Document.objects.filter(sender_status=False)
        u = CustomUser.objects.all()
        
        context = {
            'title': 'Главная страница',
            'all_users': CustomUser.objects.all().count(), # кол-во пользователей
            'all_doctors': CustomUser.objects.filter(type='DO').count(), # кол-во врачей
            'all_clients': CustomUser.objects.filter(type='CL').count(), # кол-во клиентов
            'all_active_documents': Document.objects.filter(
                Q(sender=request.user) | Q(recipient=request.user)).filter(
                    Q(sender_status=False) | Q(recipient_status=False)), # необработанные документы
            'type': DocumentType.objects.all(), # все типы документов
            'all_documents': Document.objects.all().count(), # кол-во документов
            'finish': Document.objects.all().filter(Q(sender_status=True) & Q(recipient_status=True)).count(), # кол-во подписанных документов
            'contract': Document.objects.filter(type__type_document='DOGOVOR').count(), # кол-во договоров
            'ids': Document.objects.filter(type__type_document='IDS').count(), # кол-во ИДС
            'medcard': Document.objects.filter(type__type_document='MEDCARD').count(), # кол-во медкард
            'admcard': Document.objects.filter(type__type_document='ADMCARD').count(), # кол-во адмкард
            'rent': Document.objects.filter(type__type_document='RENT').count(), # кол-во справок в налоговую
            'plan': Document.objects.filter(type__type_document='PLAN').count(), # кол-во планов лечения
            'medcarddne': Document.objects.filter(type__type_document='DNEVNIK').count(),
            # 'u': u,
        }
        
        return render(request, 'index/cabinet/di.html', context)
    
    # СТРАНИЦА ВРАЧА
    if request.user.is_authenticated and request.user.type == 'DO':
        all_types = DocumentType.objects.all()
        contract = DocumentType.objects.filter(pk=1).count()
        ids = DocumentType.objects.filter(pk=2).count()
        medcard = DocumentType.objects.filter(pk=3).count()
        admcard = DocumentType.objects.filter(pk=4).count()
        medcarddne = DocumentType.objects.filter(pk=8).count()
        rent = DocumentType.objects.filter(pk=5).count()
        plan = DocumentType.objects.filter(pk=6).count()

        context = {
            'type': all_types,
            'all_active_documents': Document.objects.filter(Q(sender=request.user) | Q(recipient=request.user)).filter(
                Q(sender_status=False) | Q(recipient_status=False)),
            'contract': contract,
            'ids': ids,
            'medcard': medcard,
            'admcard': admcard,
            'rent': rent,
            'plan': plan,

        }
        return render(request, 'index/cabinet/do.html', context)
    
    # СТРАНИЦА КЛИЕНТА
    if request.user.is_authenticated and request.user.type == 'CL':
        context = {
            #
            'all_active_documents': Document.objects.filter(Q(sender=request.user) | Q(recipient=request.user)).filter(Q(sender_status=False) | Q(recipient_status=False)),
            #'all_documents_type': all_documents_type,
        }
        return render(request, 'index/cabinet/cl.html', context)