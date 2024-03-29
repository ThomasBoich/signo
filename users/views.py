from django.contrib.auth.decorators import permission_required
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views import View
from django.db.models import Q, F, Count, Case, When, Subquery, OuterRef, Sum, IntegerField, Prefetch
from django.db.models.functions import Coalesce
from django.db import models

from documents.models import Document
from forms import SendDocumentForm
from users.forms import LoginForm, UserUpdateForm, CustomUserCreationForm, MedCardUpdateForm
from users.models import CustomUser, MedCard, Action
from .services import *
from utils.services import paginate_list


def login(request):
    pass

def registration(request):
    pass

def logout(request):
    pass


class AppLoginView(LoginView):
    form_class = LoginForm
    template_name = 'users/login.html'
    success_url = reverse_lazy('index')

    def get_success_url(self):
        return reverse_lazy('index')

    redirect_authenticated_user = True


class AppLogoutView(LogoutView):
    def get_success_url(self):
        return reverse_lazy('login')


@login_required
def staff(request):
    all_staff = CustomUser.objects.filter(Q(type='DO') | Q(type='AD'))

    all_staff = all_staff.annotate(
        signed_docs=Count(
            'sender',
            filter=Q(sender__sender_status=True),
            distinct=True)
    )
    all_staff = all_staff.annotate(
        not_signed_docs=Count(
            'sender',
            filter=Q(sender__sender_status=False),
            distinct=True)
    )
   
    
    # all_staff = all_staff \
    # .annotate(docs_sent = Subquery(Document.objects.filter(sender=OuterRef('id')).count())) \
    # .annotate(docs_found = Subquery(Document.objects.filter(founder=OuterRef('id')).count())) \
    # .annotate(difference = Subquery(Document.objects.filter(sender=OuterRef('id'), founder=OuterRef('id')).count()))
    # #.annotate(result=F('docs_found') + F('docs_sent') - F('difference'))
    

    all_staff = all_staff.annotate(
        count_sender=Subquery(
            Document.objects
                .filter(sender=OuterRef('id'))
                .exclude(founder=OuterRef('id'))
                .values('sender')
                .order_by('sender')
                .annotate(count=Count('sender'))
                .values('count')[:1],
                output_field=IntegerField()
            ),
        count_founder=Subquery(
            Document.objects
                .filter(founder=OuterRef('id'))
                .exclude(sender=OuterRef('id'))
                .values('founder')
                .order_by('founder')
                .annotate(count=Count('founder'))
                .values('count')[:1],
                output_field=models.IntegerField()
            ),
        count_both=Subquery(
            Document.objects
                .filter(founder=OuterRef('id'), sender=OuterRef('id'))
                .values('founder')
                .order_by('founder')
                .annotate(count=Count('founder'))
                .values('count')[:1],
                output_field=models.IntegerField()
            ),
        )
   
    staff = search_users(request, all_staff)

    staff = paginate_list(request, staff, 20)

    context = {
        'title': f'Сотрудники - {all_staff.count()}',
        'users': staff,
        }

    return render(request, 'index/users.html', context=context)


@login_required
def users(request):
    if request.user.type == 'ID':
        list_of_clients = Document.objects.filter(
            deleted=False,
            hidden=False
            ).values_list('recipient', flat=True)
    else:
        list_of_clients = list(Document.objects. \
                                filter(deleted=False, hidden=False). \
                                filter(Q(sender=request.user) | Q(founder=request.user)
                                ).distinct()
                                .values_list('recipient', flat=True))
    
    all_clients = CustomUser.objects.filter(id__in=list_of_clients)
    all_clients = annotate_users_with_number_of_signed_docs(
                                            all_clients, 
                                            'recipient__recipient_status')
            

    clients = search_users(request, all_clients)

    clients = paginate_list(request, clients, 20)


    context = {
        'title': 'Пациенты', # don't touch! this value is used in template
        'users': clients, 
    }
    return render (request, 'index/users.html', context=context)


# @login_required
# def administrators(request):
#     all_admins = CustomUser.objects.filter(type='AD')
#     all_admins = annotate_users_with_number_of_signed_docs(
#                                             all_admins, 
#                                             'sender__sender_status')
#     admins = search_users(request, all_admins)
#     context = {'title': 'Администраторы', 'users': admins}
#     return render(request, 'index/users.html', context=context)


@login_required
def show_profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        
        if u_form.is_valid():
            form = u_form.save(commit=False)
            form.phone = '+' + ''.join([char for char in form.phone if char.isdigit()])
            form.save()
            messages.success(request, f'Ваш профиль успешно обновлен.')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        # p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'title': 'Настройки профиля',
        'u_form': u_form,
        # 'p_form': p_form,
    }

    return render(request, 'index/profile.html', context)


@login_required
def show_mymedcard(request):
    if request.method == 'POST':
        u_form = MedCardUpdateForm(request.POST, instance=request.user.medcard)

        if u_form.is_valid():
            u_form.save()
            messages.success(request, f'Ваш профиль успешно обновлен.')
            return redirect('profile')

    else:
        u_form = MedCardUpdateForm(instance=request.user.medcard)

    context = {
        'title': 'Медицинская карта',
        'u_form': u_form,
    }

    return render(request, 'index/mymedcard.html', context)



class AppRegistration(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'users/registration.html'
    success_url = reverse_lazy('index')


def user(request, pk):
    if request.user.type not in ['DO', 'CL']:
        user = CustomUser.objects.get(pk=pk)
        context = {
            'user': user,
        }
        return render(request, 'users/user.html', context)
    return redirect('index')

def user_profile(request):
    user = CustomUser.objects.get(pk=request.user.id)
    context = {
        'user': user,
    }
    return render(request, 'users/user.html', context)


def usermedcard(request, pk):
    user = MedCard.objects.get(pk=pk)
    context = {
        'user': user,
    }
    return render(request, 'users/usermedcard.html', context)


def user_docs(request, pk):

    all_documents = Document.objects.filter(deleted=False, hidden=False, recipient=pk)
    all_documents = filter_all_documents(request, all_documents)
    all_documents = paginate_list(request, all_documents, 20)

    context = {
        'all_documents': all_documents,
        'user': CustomUser.objects.get(pk=pk),
    }

    return render(request, 'users/user-docs.html', context)


class LogsView(View):
    def get(self, request):
        actions = Action.objects.all().order_by('-pub_date')
        actions = filter_actions(request, actions)
        actions = paginate_list(request, actions, 50)

        context = {
            'title': f'Всего - {Action.objects.all().count()}',
            'actions': actions,
        }
        return render(request, 'users/logs.html', context=context)