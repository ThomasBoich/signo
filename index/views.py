from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.db.models import Q, Count, Case, When, OuterRef, Subquery, F
from django.db import models

from documents.models import Document, DocumentType
from users.models import CustomUser, Action
from users.services import *
from documents.services import *
from utils.services import paginate_list



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
                signed_by_us=Count(Case(
                    When(document__sender_status=True, then=1),
                    output_field=models.IntegerField(),
                    distinct=True
            ))).annotate(signed_by_me=Count(Case(
                    When(document__sender_status=True, document__sender=request.user, then=1),
                    output_field=models.IntegerField(),
                    distinct=True))) \
            .annotate(count_type=Count(Case(
                When(document__sender=request.user, document__deleted=False, then=1),
                output_field=models.IntegerField(),
                distinct=True)))


    types_for_do = types.exclude(
            type_document__in=['DOGOVOR', 'RENT', 'DNEVNIK']
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

    # СТРАНИЦА СУПЕРАДМИНИСТРАТОРА И АДМИНИСТРАТОРА
    if request.user.is_authenticated and (request.user.type == 'AD' or request.user.type == 'DI'):

        # annotated above
        types_for_di = types.exclude(type_document='OTKAZ')
        types_for_ad = types_for_do

        # показываем все последние документы в системе если это руководитель
        if request.user.type == 'DI':
            all_documents = all_documents
        else:
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
        my_clients = CustomUser.objects.filter(
            Q(recipient__sender=request.user) | Q(recipient__founder=request.user))
        my_clients = annotate_users_with_number_of_signed_docs(
            my_clients,
            'recipient__recipient_status').count()

        context = {
            'title': 'Главная страница',
            'all_users': CustomUser.objects.all().count(), 
            'all_admins': CustomUser.objects.filter(type='AD').count(),
            'all_doctors': CustomUser.objects.filter(type='DO').count(),
            'all_clients': my_clients if request.user.type == 'AD'
                                                else CustomUser.objects.filter(type='CL').count(),
            'all_documents': all_documents,
            
            'docs_signed_by_admins': docs_signed_by_admins,
            'docs_not_signed_by_admins': docs_not_signed_by_admins,
            'docs_signed_by_doctors': docs_signed_by_doctors,
            'docs_not_signed_by_doctors': docs_not_signed_by_doctors,
            'docs_signed_by_clients': docs_signed_by_clients,
            'docs_not_signed_by_clients': docs_not_signed_by_clients,

            'clients_with_unsigned_docs': clients_with_unsigned_docs,
            'clients_with_all_docs_signed': clients_with_all_docs_signed,

            'types' : types_for_di if request.user.type == 'DI' else types_for_ad,
            'actions': actions,
        }

        if request.user.type == 'DI':
            return render(request, 'index/cabinet/di.html', context)
        else:
            return render(request, 'index/cabinet/ad.html', context)
    
    # СТРАНИЦА ВРАЧА
    if request.user.is_authenticated and request.user.type == 'DO':
        # types can be found above
        
        all_documents = all_documents.filter(
            sender=request.user, 
            sender_status=False
            )

        # my_clients = CustomUser.objects.filter(
        #     Q(recipient__sender=request.user) | Q(recipient__founder=request.user))
        #
        # my_clients = annotate_users_with_number_of_signed_docs(
        #     my_clients,
        #     'recipient__recipient_status')

        my_clients = CustomUser.objects.filter(
            Q(recipient__sender=request.user) | Q(recipient__founder=request.user))
        my_clients = annotate_users_with_number_of_signed_docs(
            my_clients,
            'recipient__recipient_status').count()

        context = {
            'types': types,
            'all_clients': my_clients,
            'clients_with_all_docs_signed': clients_with_all_docs_signed,
            'clients_with_unsigned_docs': clients_with_unsigned_docs,
            'all_documents': all_documents,
            # 'my_clients': my_clients,
        }
        return render(request, 'index/cabinet/do.html', context)
    
    # СТРАНИЦА КЛИЕНТА
    if request.user.is_authenticated and request.user.type == 'CL':
        all_documents = all_documents.filter(
            recipient=request.user, 
            )
        context = {
            'all_documents': all_documents,
        }
        return render(request, 'index/cabinet/cl.html', context)


# СТРАНИЦА МОИ КЛИЕНТЫ
def myclients(request):

    all_users = CustomUser.objects.filter(
            Q(recipient__sender=request.user) | Q(recipient__founder=request.user))

    all_users = annotate_users_with_number_of_signed_docs(
                                            all_users,
                                            'recipient__recipient_status')
    
    users = search_users(request, all_users)

    context = {
        'title': f'Мои Пациенты - {all_users.count()}',
        'users': users,
    }
    return render(request, 'index/myclients.html', context=context)

# СТРАНИЦА ВСЕ КЛИЕНТЫ
def allclients(request):

    all_users = CustomUser.objects.filter(type='CL')
    all_users = annotate_users_with_number_of_signed_docs(
                                            all_users,
                                            'sender__sender_status')
    
    users = search_users(request, all_users)
    
    context = {
        'title': f"Пациенты - {CustomUser.objects.filter(type='CL').count()}",
        'users': users
    }
    return render(request, 'index/allclients.html', context=context)