import random
import logging
import base64
import os

from PyPDF2 import PdfReader, PdfWriter

from django.views import View
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.conf import settings
from django.core.files.base import ContentFile


from documents.models import Document, DocumentType
from forms import SendDocumentForm
from users.models import CustomUser, Action
from .services import *
from .send_sms import *
from utils.services import paginate_list
from .logger import setup_logger


logger = logging.getLogger(__name__)
setup_logger()

@login_required
def show_documents(request):
    
    all_documents = Document.objects.filter(deleted=False, hidden=False)
    if request.user.type == 'CL':
        return redirect('index')
    else:  
        all_documents = filter_all_documents(request, all_documents)

        form = SendDocumentForm(request.POST or None, request.FILES)
        if request.method == 'POST':
            if form.is_valid():
                new_doc = form.save(commit=False)
                new_doc.save()
                return redirect('documents')
        else:
            form = SendDocumentForm()

        all_documents = paginate_list(request, all_documents, 20)
        all_my_clients = Document.objects.filter(
            Q(sender=request.user) | 
            Q(founder=request.user)
            ).distinct('recipient')

        all_my_clients_signed = all_my_clients.filter(recipient_status=True)
        all_my_clients_not_signed = all_my_clients.filter(recipient_status=False)
        # types = DocumentType.objects.all().exclude(type_document='OTKAZ_OT_MED')
        types = DocumentType.objects.all()
        context = {
            'title': f'Все Документы - {Document.objects.all().filter(deleted=False, hidden=False).count()}',
            'form': form,
            'doc_title': 'Отправить на подпись',
            'all_users': CustomUser.objects.all().count(),
            'all_doctors': CustomUser.objects.filter(type='DO').count(),
            'all_clients': CustomUser.objects.filter(type='CL').count(),
            'all_my_clients': all_my_clients.count(),
            'all_my_clients_signed': all_my_clients_signed.count(),
            'all_my_clients_not_signed': all_my_clients_not_signed.count(),
            'all_documents': all_documents,
            'types': types,
            }
        return render(request, 'documents/documents.html', context=context)


@login_required
def show_category(request, pk):
    form = SendDocumentForm(request.POST or None, request.FILES)
    if request.method == 'POST':
        if form.is_valid():
            new_doc = form.save(commit=False)
            # new_doc.sender = request.user
            new_doc.save()
            return redirect('documents')
    else:
        form = SendDocumentForm()

    context = {
        'title': '',
        'form': form,
        'documents': '',

    }
    return render(request, 'documents/category.html', context=context)

@login_required
def mydocuments(request):
    all_documents = Document.objects. \
        filter(deleted=False, hidden=False). \
        filter(Q(recipient=request.user) | Q(sender=request.user))
    all_documents = filter_all_documents(request, all_documents)
    all_documents_count = all_documents.count()
    all_documents = paginate_list(request, all_documents, 20)

    types = DocumentType.objects.all().exclude(type_document='OTKAZ_OT_MED')

    form = SendDocumentForm(request.POST or None, request.FILES)
    if request.method == 'POST':
        if form.is_valid():
            new_doc = form.save(commit=False)
            new_doc.save()
            return redirect('documents')
    else:
        form = SendDocumentForm()

    all_my_clients = Document.objects.filter(
        Q(sender=request.user) | 
        Q(founder=request.user)
        ).distinct('recipient')
    print('!', all_my_clients)
    
    all_my_clients_signed = all_my_clients.filter(recipient_status=True)
    all_my_clients_not_signed = all_my_clients.filter(recipient_status=False)

    context = {
        'title': f'Мои Документы - {all_documents_count}',
        'form': form,
        'doc_title': 'Отправить на подпись',
        'all_users': CustomUser.objects.all().count(),
        'all_doctors': CustomUser.objects.filter(type='DO').count(),
        'all_clients': CustomUser.objects.filter(type='CL').count(),
        'all_my_clients': all_my_clients.count(),
        'all_my_clients_signed': all_my_clients_signed.count(),
        'all_my_clients_not_signed': all_my_clients_not_signed.count(),
        'all_documents': all_documents,
        'types': types,
        }
    if not request.user.type == 'CL':
        return render(request, 'documents/mydocuments.html', context=context)
    else:
        return redirect('/')





def send_code(request):
    code = random.randrange(1000, 9999)
    request.session['code'] = code
    phone = request.user.phone.replace('+', '')
    send_code_to_phone(phone, code)
    return JsonResponse({'code':'sent'})


def sign_document(request):
    try:
        code_entered = int(request.POST.get('code'))
        code_sent = request.session['code']
    except:
        code_entered, code_sent = 0, 0
    pk = request.POST.get('doc_id')

    if (request.user.type == 'CL' and code_entered == code_sent) or request.user.type in ['DO', 'AD']:
        document = Document.objects.get(pk=pk)
        create_signature(request, document)
        
        media_root = settings.MEDIA_ROOT
        
        watermark = media_root + "/signature" + str(document.id) + ".pdf"
        
        doc_file = document.document.path

        with open(doc_file, "rb") as input_file, open(watermark, "rb") as watermark_file:
            input_pdf = PdfReader(input_file)
            watermark_pdf = PdfReader(watermark_file)
            watermark_page = watermark_pdf.pages[0]

            output = PdfWriter()
            for i in range(len(input_pdf.pages)):
                pdf_page = input_pdf.pages[i]
                pdf_page.merge_page(watermark_page)
                output.add_page(pdf_page)

            with open(doc_file, "wb") as merged_file:
                output.write(merged_file)

            if request.user.type == 'CL':
                document.recipient_status = True
                document.save()
                Action.objects.create(
                    action=f'{request.user.first_name} {request.user.last_name} \
                        подписал {document.type.get_type_document_display()} с {document.sender.first_name} \
                        {document.sender.last_name}'
                    )
            else:
                document.sender_status = True
                document.save()
                Action.objects.create(
                    action=f'{request.user.first_name} {request.user.last_name} \
                        подписал {document.type.get_type_document_display()} с {document.recipient.first_name} \
                        {document.recipient.last_name}'
                    )

        if os.path.exists(watermark):
            os.remove(watermark)
         
        result = {'reload': 'y'} # used on the front as a sign to reload page
        return JsonResponse(result)
    
    result = {'code': ''}

    return JsonResponse(result)


def delete_document(request):
    if request.method == 'POST':
        document_pk = request.POST.get('document_pk')
        document = Document.objects.get(id=document_pk)
        document.deleted = True
        document.save()
        user=request.user
        Action.objects.create(
            action=f'{user.first_name} {user.last_name} удалил {document.type.get_type_document_display()} ({document})')
    return HttpResponse(status=204)



# def get_doc_to_frontend(request):
#     doc_id = request.GET.get('doc_id')
    
#     doc = Document.objects.get(id=doc_id)
#     doc_file = doc.document.open('rb')
#     b_doc = base64.b64encode(doc_file.read())
    
#     return JsonResponse({'file': b_doc})


class SaveSigView(View):
    def post(self, request):
        doc_id = request.POST.get('doc_id')
        doc = Document.objects.get(id=doc_id)
        sig = request.POST.get('sig')
        
        doc.sender_status = True
        doc.save()
        
        file_name = doc_id + '.sig'   
        my_file = ContentFile(sig)
        doc.sig.save(file_name, my_file)

        sign_document(request)

        return HttpResponse('')

        