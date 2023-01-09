from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.db.models import Q, Count, When, Case, Subquery, OuterRef
from django.db import models

from documents.models import Document
from users.forms import LoginForm, ProfileUpdateForm, UserUpdateForm, CustomUserCreationForm, MedCardUpdateForm
from users.models import CustomUser, MedCard
from .services import *


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
def doctors(request):
    context = {'title': 'Врачи', 'users': CustomUser.objects.filter(type='DO')}
    return render(request, 'index/doctors.html', context=context)


@login_required
def users(request):
    
    list_of_clients = list(Document.objects.filter(
            Q(sender=request.user) | Q(founder=request.user)
            ).distinct()
            .values_list('recipient', flat=True))
    
    all_clients = CustomUser.objects.filter(id__in=list_of_clients) \
            .annotate(
                signed_docs=Count(Case(
                    When(recipient__recipient_status=True, then=1),
                    output_field=models.IntegerField(),
                    distinct=True
            ))) \
            .annotate(
                not_signed_docs=Count(Case(
                    When(recipient__recipient_status=False, then=1),
                    output_field=models.IntegerField(),
                    distinct=True
            )))

    clients = search_users(request, all_clients)

    sort_filter = request.GET.get('sort')
    print('!', sort_filter)
    if sort_filter:
        clients = clients.order_by(sort_filter)

    context = {
        'title': 'Клиенты',
        'users': clients, 
    }
    return render (request, 'index/users.html', context=context)


@login_required
def administrators(request):
    context = {'title': 'Администраторы', 'users': CustomUser.objects.filter(type='AD')}
    return render(request, 'index/administrators.html', context=context)


@login_required
def show_profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        # p_form = ProfileUpdateForm(request.POST,
        #                            request.FILES,
        #                            instance=request.user.profile)
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
        # p_form = ProfileUpdateForm(request.POST,
        #                            request.FILES,
        #                            instance=request.user.profile)
        if u_form.is_valid():
            u_form.save()
            # p_form.save() and p_form.is_valid()
            messages.success(request, f'Ваш профиль успешно обновлен.')
            return redirect('profile')

    else:
        u_form = MedCardUpdateForm(instance=request.user.medcard)
        # p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'title': 'Медицинская карта',
        'u_form': u_form,
        # 'p_form': p_form,
    }

    return render(request, 'index/mymedcard.html', context)



class AppRegistration(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'users/registration.html'
    success_url = reverse_lazy('index')


def user(request, pk):
    user = CustomUser.objects.get(pk=pk)
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


