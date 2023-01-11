from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.db.models import Q, Count, Case, When, OuterRef, Subquery
from django.db import models

from documents.models import Document, DocumentType
from users.models import CustomUser


@login_required
def index(request):
    ''' ГЛАВНАЯ СТРАНИЦА С ИНФОГРАФИКОЙ '''
    if request.user.is_authenticated == False:
        return redirect('login')
    # else:
        # all_documents_type = DocumentType.objects.all().count()
        
 
    
    # СТРАНИЦА СУПЕРАДМИНИСТРАТОРА И АДМИНИСТРАТОРА
    if request.user.is_authenticated and (request.user.type == 'AD' or request.user.type == 'DI'):
        g = Document.objects.filter(sender_status=False)

        
        # добавляем поля "подписано доктором" и "подписано пациентом"
        types = DocumentType.objects.all() \
            .exclude(type_document='OTKAZ') \
            .annotate(
                signed_by_patient=Count(Case(
                    When(document__recipient_status=True, then=1),
                    output_field=models.IntegerField(), 
                    distinct=True
            ))) \
            .annotate(
                signed_by_doctor=Count(Case(
                    When(document__sender_status=True, then=1),
                    output_field=models.IntegerField(),
                    distinct=True
            )))
        docs_signed_by_admins = Document.objects.filter(
                                    sender__type='AD', 
                                    sender_status=True
                                    ).count()
        docs_not_signed_by_admins = Document.objects.filter(
                                    sender__type='AD', 
                                    sender_status=False
                                    ).count()
        docs_signed_by_doctors = Document.objects.filter(
                                    sender__type='DO', 
                                    sender_status=True
                                    ).count()
        docs_not_signed_by_doctors = Document.objects.filter(
                                    sender__type='DO', 
                                    sender_status=False
                                    ).count()
        docs_signed_by_clients = Document.objects.filter(
                                    recipient__type='CL', 
                                    recipient_status=True
                                    ).count()
        docs_not_signed_by_clients = Document.objects.filter(
                                        recipient__type='CL', 
                                        recipient_status=False
                                        ).count()
        context = {
            'title': 'Главная страница',
            'all_users': CustomUser.objects.all().count(), # кол-во пользователей
            'all_admins': CustomUser.objects.filter(type='AD').count(), # кол-во врачей
            'all_doctors': CustomUser.objects.filter(type='DO').count(), # кол-во врачей
            'all_clients': CustomUser.objects.filter(type='CL').count(), # кол-во клиентов
            'all_active_documents': Document.objects.filter(
                Q(sender=request.user) | Q(recipient=request.user)).filter(
                    Q(sender_status=False) | Q(recipient_status=False)).order_by('-id'), # необработанные документы
            'all_documents': Document.objects.all().count(), # кол-во документов
            'docs_signed_by_admins': docs_signed_by_admins,
            'docs_not_signed_by_admins': docs_not_signed_by_admins,
            'docs_signed_by_doctors': docs_signed_by_doctors,
            'docs_not_signed_by_doctors': docs_not_signed_by_doctors,
            'docs_signed_by_clients': docs_signed_by_clients,
            'docs_not_signed_by_clients': docs_not_signed_by_clients,
            'finish': Document.objects.all().filter(Q(sender_status=True) & Q(recipient_status=True)).count(), # кол-во подписанных документов
            'types' : types,
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


# СТРАНИЦА МОИ КЛИЕНТЫ
def myclients(request):
    context = {
        'title': 'Мои Пациенты',
        'users': CustomUser.objects.filter(), # - здесь вывести всемх клиентов врача и администратора, для sender и founder
    }
    return render(request, 'index/myclients.html', context=context)