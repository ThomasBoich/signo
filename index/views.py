from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.db.models import Q, Count, Case, When, OuterRef, Subquery
from django.db import models

from documents.models import Document, DocumentType
from users.models import CustomUser, Action
from documents.services import *


@login_required
def index(request):
    ''' ГЛАВНАЯ СТРАНИЦА С ИНФОГРАФИКОЙ '''
    if request.user.is_authenticated == False:
        return redirect('login')
    # else:
        # all_documents_type = DocumentType.objects.all().count()
        
 
    
    # СТРАНИЦА СУПЕРАДМИНИСТРАТОРА И АДМИНИСТРАТОРА
    if request.user.is_authenticated and (request.user.type == 'AD' or request.user.type == 'DI'):
        g = Document.objects.filter(deleted=False, sender_status=False)

        all_documents = Document.objects. \
            filter(deleted=False). \
            filter(
                Q(sender=request.user) | Q(recipient=request.user) &
                (Q(sender_status=False) | Q(recipient_status=False))
                )
        all_documents = filter_all_documents(request, all_documents)
        
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

        signed_docs = Document.objects.filter(deleted=False)
        docs_signed_by_admins = signed_docs.filter(
                                    sender__type='AD', 
                                    sender_status=True
                                    ).count()
        docs_not_signed_by_admins = signed_docs.filter(
                                    sender__type='AD', 
                                    sender_status=False
                                    ).count()
        docs_signed_by_doctors = signed_docs.filter(
                                    sender__type='DO', 
                                    sender_status=True
                                    ).count()
        docs_not_signed_by_doctors = signed_docs.filter(
                                    sender__type='DO', 
                                    sender_status=False
                                    ).count()
        docs_signed_by_clients = signed_docs.filter(
                                    recipient__type='CL', 
                                    recipient_status=True
                                    ).count()
        docs_not_signed_by_clients = signed_docs.filter(
                                        recipient__type='CL', 
                                        recipient_status=False
                                        ).count()

        actions = Action.objects.all().order_by('-pub_date')[:5]
        context = {
            'title': 'Главная страница',
            'all_users': CustomUser.objects.all().count(), # кол-во пользователей
            'all_admins': CustomUser.objects.filter(type='AD').count(), # кол-во врачей
            'all_doctors': CustomUser.objects.filter(type='DO').count(), # кол-во врачей
            'all_clients': CustomUser.objects.filter(type='CL').count(), # кол-во клиентов
            'all_documents': all_documents,
            'docs_signed_by_admins': docs_signed_by_admins,
            'docs_not_signed_by_admins': docs_not_signed_by_admins,
            'docs_signed_by_doctors': docs_signed_by_doctors,
            'docs_not_signed_by_doctors': docs_not_signed_by_doctors,
            'docs_signed_by_clients': docs_signed_by_clients,
            'docs_not_signed_by_clients': docs_not_signed_by_clients,
            'types' : types,
            'actions': actions,
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
        }
        return render(request, 'index/cabinet/cl.html', context)


# СТРАНИЦА МОИ КЛИЕНТЫ
def myclients(request):
    context = {
        'title': 'Мои Пациенты',
        'users': CustomUser.objects.filter(), # - здесь вывести всемх клиентов врача и администратора, для sender и founder
    }
    return render(request, 'index/myclients.html', context=context)