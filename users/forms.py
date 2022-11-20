from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm

from .models import CustomUser, Profile, MedCard


class CustomUserCreationForm(UserCreationForm):

    # email = forms.CharField(label='Логин', widget=forms.EmailInput(attrs={'class': 'form-control'}))
    # first_name = forms.CharField(label='Имя', widget=forms.TextInput(attrs={'class': 'form-control'}))
    # last_name = forms.CharField(label='Фамилия', widget=forms.TextInput(attrs={'class': 'form-control'}))
    # # password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    # # password2 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    # patronymic = forms.CharField(label='Отчество', required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    # pasport_series = forms.CharField(label='Серия паспорта', required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    # pasport_number = forms.CharField(label='Номер паспорта', required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    # phone = forms.CharField(label='Телефон', required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    # addres = forms.CharField(label='Адрес', required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))


    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('email', 'pasport_series', 'pasport_number', 'phone', 'first_name', 'last_name', 'patronymic')


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'patronymic', 'pasport_series', 'pasport_number', 'phone', 'addres']


class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Электронная почта', widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    class Meta:
        model = CustomUser
        fields = ['email', 'username', 'password']


# class RegistrationForm(forms.ModelForm):
#     # username = forms.CharField(label='Логин', widget=forms.EmailInput(attrs={'class': 'form-control'}))
#     # first_name = forms.CharField(label='Имя', widget=forms.TextInput(attrs={'class': 'form-control'}))
#     # last_name = forms.CharField(label='Фамилия', widget=forms.TextInput(attrs={'class': 'form-control'}))
#     # password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
#     # password2 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
#     # patronymic = forms.CharField(label='Отчество', required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
#     # pasport_series = forms.CharField(label='Серия паспорта', required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
#     # pasport_number = forms.CharField(label='Номер паспорта', required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
#     # phone = forms.CharField(label='Телефон', required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
#     # addres = forms.CharField(label='Адрес', required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
#
#     class Meta(UserCreationForm.Meta):
#         model = CustomUser
#         fields = ['email', 'first_name', 'last_name', 'patronymic', 'pasport_series', 'pasport_number', 'phone', 'password1', 'password2']
#
#     def clean_password2(self):
#         cd = self.cleaned_data
#         if cd['password'] != cd['password2']:
#             raise forms.ValidationError('Passwords don\'t match.')
#         return cd['password2']

class ProfileRegisterForm(forms.ModelForm):
    # pasport_series = forms.CharField(label='Серия паспорта', required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    # pasport_number = forms.CharField(label='Номер паспорта', required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    # phone = forms.CharField(label='Номер паспорта', required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Profile
        fields = '__all__'
        # fields = ['pasport_series', 'pasport_number', 'phone']


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(label='Электронная почта', required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    # username = forms.CharField(label='Логин', required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(label='Имя', required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(label='Фамилия', required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    patronymic = forms.CharField(label='Отчество', required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    pasport_series = forms.CharField(label='Серия паспорта', required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    pasport_number = forms.CharField(label='Номер паспорта', required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    phone = forms.CharField(label='Телефон', required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    addres = forms.CharField(label='Адрес', required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    # password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'patronymic', 'pasport_series', 'pasport_number', 'phone', 'addres']
        exclude = ['username', 'sender']

class ProfileUpdateForm(forms.ModelForm):
    # photo = forms.ImageField(label='Фотография', widget=forms.FileInput(attrs={'class': 'form-control'}))
    # pasport_series = forms.CharField(label='Серия паспорта', required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    # pasport_number = forms.CharField(label='Номер паспорта', required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    # adress = forms.CharField(label='Адрес', required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    # phone = forms.CharField(label='Телефон', required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    # pasport_seriespasport_numberСерияпаспортаНомерпаспорта password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    class Meta:
        model = Profile
        fields = '__all__'
        # fields = [ 'adress', 'phone', 'pasport_series', 'pasport_number', 'photo',]

class MedCardUpdateForm(forms.ModelForm):
    # email = forms.EmailField(label='Электронная почта', required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    # password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    # username = forms.CharField(label='Логин', required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    height = forms.CharField(label='Рост', required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    weight = forms.CharField(label='Вес', required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    blood = forms.CharField(label='Группа Крови', required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    age = forms.CharField(label='Возраст', required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = MedCard
        # fields = '__all__'
        fields = ['height', 'weight', 'blood', 'age']