from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView

from users.forms import LoginForm, ProfileUpdateForm, UserUpdateForm, CustomUserCreationForm, MedCardUpdateForm
from users.models import CustomUser, MedCard


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
    context = {'title': 'Клиенты', 'users': CustomUser.objects.filter(type='CL')}
    return render (request, 'index/users.html', context=context)


@login_required
def administrators(request):
    context = {'title': 'Администраторы', 'users': CustomUser.objects.filter(type='AD')}
    return render(request, 'index/administrators.html', context=context)

# class ShowProfileView(DetailView):
#     model = Profile
#     template_name = 'index/profile.html'
#     pk_url_kwarg = 'pk'

@login_required
def show_profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        # p_form = ProfileUpdateForm(request.POST,
        #                            request.FILES,
        #                            instance=request.user.profile)
        if u_form.is_valid():
            u_form.save()
            # p_form.save() and p_form.is_valid()
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


# def AppRegistration(request):
#     if request.method == 'POST':
#         form = RegistrationForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             messages.success(request, f'Your account has been sent for approval!')
#             return redirect('index')
#     else:
#         form = RegistrationForm()
#
#     context = {
#         'form': form,
#     }
#     return render(request, 'users/registration.html', context)


class AppRegistration(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'users/registration.html'
    success_url = reverse_lazy('index')

# def AppRegistration(request):
#     if request.method == 'POST':
#         user_form = CustomUserCreationForm(request.POST)
#         if user_form.is_valid():
#             # Create a new user object but avoid saving it yet
#             new_user = user_form.save(commit=False)
#             # Set the chosen password
#             new_user.set_password(user_form.cleaned_data['password'])
#             # Save the User object
#             new_user.save()
#             return redirect('index')
#     else:
#         user_form = CustomUserCreationForm()
#     return render(request, 'users/registration.html', {'user_form': user_form})
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