import os

from django.db import models

# Create your models here.
from django.urls import reverse

from users.models import CustomUser


class Document(models.Model):
    # title = models.CharField(max_length=240, )
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, related_name='sender', verbose_name='Отправитель')
    recipient = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, related_name='recipient', verbose_name='Получатель')
    document = models.FileField(upload_to='documents/%Y/%m/%d/', blank=True, null=True)
    send_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата отправки', null=True)
    sender_status = models.BooleanField(default=False, blank=True, null=True)
    recipient_status = models.BooleanField(default=False, blank=True, null=True)
    files = models.ForeignKey('DocumentsFiles', on_delete=models.CASCADE, blank=True, null=True)
    type = models.ForeignKey('DocumentType', on_delete=models.CASCADE, blank=True, null=True, related_name='document')


    TYPE_DOC = (
        ('Договор', 'Договор'),
        ('ИДС', 'ИДС'),
        ('Мед.карта', 'Мед карта'),
        ('Адм.карта', 'Адм.карта'),
        ('Справка в налоговую', 'Справка в налоговую'),
        ('План лечения', 'План лечения')
    )

    type_document = models.CharField(choices=TYPE_DOC, max_length=240, blank=True, null=True)

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

    def count(self):
        return Document.objects.all().count()

    def count_sender(self):
        return Document.objects.filter(sender_status=True).count()

    def count_recipient(self):
        return Document.objects.filter(recipient_status=True).count()


class DocumentsFiles(models.Model):
    file = models.FileField(upload_to='documents/%Y/%m/%d/')


class DocumentType(models.Model):
    title = models.CharField(max_length=240, blank=True, null=True)

    class Meta:
        verbose_name='Тип Документа'
        verbose_name_plural='Типы Документов'
    def __str__(self):
        return self.title
    def count(self):
        DocumentType.objects.all().count