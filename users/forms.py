from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from django.core.exceptions import ValidationError

from .models import CustomUser, Profile, MedCard


class CustomUserCreationForm(UserCreationForm):
    phone = forms.CharField(label='Телефон', required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+7 999 123-45-67'}))

    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('email', 'pasport_series', 'pasport_number', 'last_name', 'first_name', 'patronymic', 'phone', 'date_of_birthday')

        widgets = {
                'date_of_birthday': forms.DateInput(attrs={"class":"form-control", "type": "date", "required":True}),
            }



    def clean(self):
        phone = self.cleaned_data['phone']
        phone = '+' + ''.join([char for char in phone if char.isdigit()])

        
class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'patronymic', 'pasport_series', 'pasport_number', 'phone', 'addres']


class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Электронная почта', widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise ValidationError(
                "This account is inactive.",
                code='inactive',
            )
        if user.ban:
            raise ValidationError(
                "Вы не можете войти, обратитесь к администратору",
                code='fired',
            )

    class Meta:
        model = CustomUser
        fields = ['email', 'username', 'password']


    

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
    class Meta:
        model = Profile
        fields = '__all__'
        # fields = [ 'adress', 'phone', 'pasport_series', 'pasport_number', 'photo',]

class MedCardUpdateForm(forms.ModelForm):
    height = forms.CharField(label='Рост', required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    weight = forms.CharField(label='Вес', required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    blood = forms.CharField(label='Группа Крови', required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    age = forms.CharField(label='Возраст', required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = MedCard
        # fields = '__all__'
        fields = ['height', 'weight', 'blood', 'age']