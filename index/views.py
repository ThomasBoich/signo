from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.db.models import Q, Count, Case, When, OuterRef, Subquery, F
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
        
    all_documents = Document.objects.filter(deleted=False)

    types = DocumentType.objects.all() \
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
    # СТРАНИЦА СУПЕРАДМИНИСТРАТОРА И АДМИНИСТРАТОРА
    if request.user.is_authenticated and (request.user.type == 'AD' or request.user.type == 'DI'):
        g = Document.objects.filter(deleted=False, sender_status=False)

        types = types.exclude(type_document='OTKAZ')

        all_documents = all_documents.filter(
                Q(sender=request.user) | Q(recipient=request.user) &
                (Q(sender_status=False) | Q(recipient_status=False))
                )
        all_documents = filter_all_documents(request, all_documents)
        
        # добавляем поля "подписано доктором" и "подписано пациентом"
        

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
        types = types.exclude(type_document__in=['DOGOVOR', 'RENT', 'DNEVNIK'])
        
        all_documents = all_documents.filter(
            sender=request.user, 
            sender_status=False
            )

        all_clients = CustomUser.objects.filter(
            type='CL', 
            recipient__sender=request.user
            )

        

        all_clients = CustomUser.objects.filter(
            type='CL', 
            recipient__sender=request.user
            ).annotate(
                signed_by_patient=Count(Case(
                    When(recipient__recipient_status=True, recipient__sender=request.user, then=1),
                    output_field=models.IntegerField(), 
                    distinct=True
            ))) \
            .annotate(
                not_signed_by_patient=Count(Case(
                    When(recipient__recipient_status=False, recipient__sender=request.user, then=1),
                    output_field=models.IntegerField(),
                    distinct=True
            ))).annotate(
                total_docs=Count('recipient')
            )
        
        clients_with_all_docs_signed = all_clients.filter(total_docs=F('signed_by_patient')).count()

        clients_with_unsigned_docs = all_clients.filter(~Q(total_docs=F('signed_by_patient'))).count()                                

        context = {
            'types': types,
            'all_clients': all_clients.count(),
            'clients_with_all_docs_signed': clients_with_all_docs_signed,
            'clients_with_unsigned_docs': clients_with_unsigned_docs,
            'all_documents': all_documents,
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