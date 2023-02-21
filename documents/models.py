import os
from django.db import models
from django.db.models.signals import post_save
from django.urls import reverse
from django.dispatch import receiver

from users.models import CustomUser, Action
from utils.models import *


# Документ
class Document(DateTimeMixin, HiddenDeletedMixin, models.Model):
    # title = models.CharField(max_length=240, )
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True, related_name='documenter')
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, related_name='sender', verbose_name='Отправитель')
    recipient = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, related_name='recipient', verbose_name='Получатель')
    founder = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, related_name='founder', verbose_name='Создатель документа')
    document = models.FileField(upload_to='documents/%Y/%m/%d/', blank=True, null=True)
    send_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата отправки', null=True)
    sender_status = models.BooleanField(default=False, blank=True, null=True)
    recipient_status = models.BooleanField(default=False, blank=True, null=True)
    files = models.ForeignKey('DocumentsFiles', on_delete=models.CASCADE, blank=True, null=True)
    type = models.ForeignKey('DocumentType', on_delete=models.CASCADE, blank=True, null=True, related_name='document')

   
    class Meta:
        verbose_name = 'Документ'
        verbose_name_plural = 'Документы'

    def __str__(self):
        # return self.title
        return f'отправитель: {self.sender} получатель: {self.recipient}'

    def get_absolute_url(self):
        return reverse('show_document', kwargs={'pk': self.pk})

    def filename(self):
        return os.path.basename(self.document.name)


class DocumentsFiles(models.Model):
    file = models.FileField(upload_to='documents/%Y/%m/%d/')


class DocumentType(models.Model):
    title = models.CharField(max_length=240, blank=True, null=True)

    DOGOVOR = 'DOGOVOR'
    IDS = 'IDS'
    MEDCARD = 'MEDCARD'
    ADMCARD = 'ADMCARD'
    RENT = 'RENT'
    PLAN = 'PLAN'
    DNEVNIK = 'DNEVNIK'
    OTKAZ = 'OTKAZ'


    TYPE_DOC = (
        (DOGOVOR, 'Договор'),
        (IDS, 'ИДС'),
        (MEDCARD, 'Мед карта'),
        (ADMCARD, 'Адм.карта'),
        (RENT, 'Справка в налоговую'),
        (PLAN, 'План лечения'),
        (DNEVNIK, 'Дневник'),
        (OTKAZ, 'Отказ от мед.вмешательства')
    )
    type_document = models.CharField(choices=TYPE_DOC, max_length=240, blank=True, null=True)

    class Meta:
        verbose_name='Тип Документа'
        verbose_name_plural='Типы Документов'

    def __str__(self):
        return self.title

    def count(self, type_document):
        DocumentType.objects.all().count()

    def get_absolute_url(self):
        return reverse('show_types', kwargs={'pk': self.pk})




# signals for logs - creating documents
# we don't actually delete documents, but rather change their 'deleted' state
# so logs for these actions are created in views. 
# Same is true for signing documents.

# @receiver(post_save, sender=Document)    
# def create_document_created_action(sender, instance, created, **kwargs):
#     if created:
#         document = instance
#         Action.objects.create(
#             action=f'{document.founder.first_name} {document.founder.last_name} ({document.founder.type}) отправил {document.type.get_type_document_display()}. Получатель {document.recipient.first_name} {document.recipient.last_name}'
#             )