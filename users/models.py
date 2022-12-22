from django.db import models
from django.contrib.auth.models import AbstractBaseUser, Permission, Group
from django.contrib.auth.models import PermissionsMixin
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from .managers import CustomUserManager

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=254, unique=True, verbose_name='Электронная почта')
    # password = models.CharField(_("password"), max_length=255, null=False)
    first_name = models.CharField(u"Имя", max_length=100, blank=True, null=True)
    last_name = models.CharField(u"Фамилия", max_length=100, blank=True, null=True)
    patronymic = models.CharField(u"Отчество", max_length=100, blank=True, null=True)
    pasport_series = models.CharField(max_length=12, blank=True, verbose_name='Серия паспорта')
    pasport_number = models.CharField(max_length=12, blank=True, verbose_name='Номер паспорта')
    addres = models.CharField(max_length=240, blank=True, verbose_name='Адрес пользователя')
    user_profile_id = models.IntegerField(blank=True, verbose_name='ID пользователя', null=True)
    phone = models.CharField(max_length=12, blank=True, null=True, verbose_name='Телефон')
    uniq_id = models.CharField(max_length=12, blank=True, null=True, verbose_name='Уникальный ID')
    photo = models.ImageField(upload_to='midia/users/%Y/%m/%d/', blank=True, default='media/users/use.png', verbose_name='Аватар')
    # role = models.ForeignKey('Role', on_delete=models.CASCADE, blank=True, null=True, default=3)
    ## document = models.ForeignKey('Documents', on_delete=models.CASCADE, blank=True, null=True)
    is_active = models.BooleanField(default=True, verbose_name='Активирован')
    is_admin = models.BooleanField(default=False, verbose_name='Администратор')
    is_staff = models.BooleanField(_('staff status'), default=False)
    is_superuser = models.BooleanField(_('super user'), default=False)
    date_joined = models.DateTimeField(u'date joined', blank=True, null=True, default=timezone.now)
    last_login = models.DateTimeField(u'last login', blank=True, null=True)
    groups = models.ManyToManyField(Group, blank=True, null=True, verbose_name='Группы', related_name='groups')
    user_permissions = models.ManyToManyField(Permission, blank=True, null=True, verbose_name='Разрешения', related_name='user_permissions')
    outside = models.DateTimeField(verbose_name='дата увольнения', blank=True, null=True)
    
    ADMINISTRATOR = 'AD'
    DOCTOR = 'DO'
    CLIENT = 'CL'
    DIRECTOR = 'DI'

    TYPE_ROLE = [
        (ADMINISTRATOR, 'Администратор'),
        (DOCTOR, 'Доктор'),
        (CLIENT, 'Клиент'),
        (DIRECTOR, 'Руководитель')
    ]

    type = models.CharField(max_length=6, choices=TYPE_ROLE, default=CLIENT, verbose_name='Тип пользователя')
    ban = models.BooleanField(default=False, verbose_name='Уволен')
    ecp = models.BooleanField(default=False, verbose_name='Наличие ЭЦП')
    logs = models.BooleanField(default=True, blank=True, verbose_name='Доступ к вкладке логи')
    delete = models.BooleanField(default=True, blank=True, verbose_name='Доступ к удалению документов')
    downloads = models.BooleanField(default=True, blank=True, verbose_name='Доступ к скачиванию документов')
    views = models.BooleanField(default=True, blank=True, verbose_name='Доступ к просмотру документов')
    phones = models.BooleanField(default=True, blank=True, verbose_name='Доступ к просмотру телефонов')
    pasports = models.BooleanField(default=True, blank=True, verbose_name='Доступ к паспортным данным')
    documents = models.BooleanField(default='True', blank=True, verbose_name='Доступ к вкладке документы')
    settings = models.BooleanField(default='True', blank=True, verbose_name='Доступ к вкладке настройка пользователей')
    all_info = models.BooleanField(default='True', blank=True, verbose_name='Доступ к информации о всех пациентах')
    my_info = models.BooleanField(default='True', blank=True, verbose_name='Доступ к информации о своих пациентах')
   
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return f'{self.first_name} {self.last_name} {self.patronymic}'

    class Meta:
        verbose_name='Пользователь'
        verbose_name_plural='Пользователи'

    def get_absolute_url(self):
        return reverse('user', kwargs={'pk': self.pk})


# ПРОФИЛЬ ПОЛЬЗОВАТЕЛЯ С ДОПОЛНИТЕЛЬНОЙ ИНФОРМАЦИЕЙ #
class Profile(models.Model):

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return f" {self.user.first_name} {self.user.last_name}"

    class Meta:
        verbose_name = 'Профиль пользователя'
        verbose_name_plural = 'Профили пользователей'

    def get_absolute_url(self):
        return reverse('profile', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def first_name(self):
        return self.user.first_name


class MedCard(models.Model):
    user = models.OneToOneField(CustomUser, verbose_name='Клиент', on_delete=models.CASCADE)
    height = models.CharField(max_length=100, verbose_name='Рост', blank=True, null=True)
    weight = models.CharField(max_length=100, verbose_name='Вес', blank=True, null=True)
    blood = models.CharField(max_length=100, verbose_name='Группа крови', blank=True, null=True)
    age = models.CharField(max_length=100, verbose_name='Возраст', blank=True, null=True)

    def __str__(self):
        return f'{self.user}, {self.user.first_name} {self.user.last_name}'

    class Meta:
        verbose_name = 'Карта'
        verbose_name_plural = 'Карты'


@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        MedCard.objects.create(user=instance)


@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
    instance.medcard.save()


class Vizit(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True, verbose_name='Клиент', related_name='vizit_client')
    doctor = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True, verbose_name='Врач', related_name='vizit_doctor')
    title = models.CharField(max_length=240, blank=True, null=True, verbose_name='Цель визита')
    documents = models.FileField(upload_to='media/%Y/%m/%d/', blank=True, null=True)
    info = models.TextField(blank=True, null=True, verbose_name='Жалобы')
    purpose = models.TextField(blank=True, null=True, verbose_name='Цель визита')
    date_purpose = models.DateTimeField(blank=True, null=True, verbose_name='Дата посещения')
    status = models.BooleanField(default=True, verbose_name='Посещение завершено')

    def __str__(self):
        return f'{self.user.first_name},{self.user.last_name}, {self.title}'

    class Meta:
        verbose_name = 'Визит'
        verbose_name_plural = 'Визиты'


class CustomPermissions(models.Model):
    logs = models.BooleanField(default=True, verbose_name='Доступ к вкладке логи')
    delete = models.BooleanField(default=True, verbose_name='Доступ к удалению документов')
    downloads = models.BooleanField(default=True, verbose_name='Доступ к скачиванию документов')
    views = models.BooleanField(default=True, verbose_name='Доступ к просмотру документов')
    phones = models.BooleanField(default=True, verbose_name='Доступ к просмотру телефонов')
    pasports = models.BooleanField(default=True, verbose_name='Доступ к паспортным данным')
    documents = models.BooleanField(default='True', verbose_name='Доступ к вкладке документы')
    settings = models.BooleanField(default='True', verbose_name='Доступ к вкладке настройка пользователей')
    all_info = models.BooleanField(default='True', verbose_name='Доступ к информации о всех пациентах')
    my_info = models.BooleanField(default='True', verbose_name='Доступ к информации о своих пациентах')

from documents.models import *