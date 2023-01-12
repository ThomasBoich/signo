import random
from PyPDF2 import PdfReader, PdfWriter

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse
from django.conf import settings

from documents.models import Document, DocumentType
from forms import SendDocumentForm
from users.models import CustomUser
from .services import *
from .send_sms import *


@login_required
def show_documents(request):
    
    all_documents = Document.objects.all()
    
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


        types = DocumentType.objects.all().exclude(type_document='OTKAZ')
        context = {
            'title': 'Все Документы',
            'form': form,
            'doc_title': 'Отправить на подпись',
            'all_users': CustomUser.objects.all().count(),
            'all_doctors': CustomUser.objects.filter(type='DO').count(),
            'all_clients': CustomUser.objects.filter(type='CL').count(),
            'all_active_documents': Document.objects.filter(
                Q(sender=request.user) | Q(recipient=request.user)).filter(
                Q(sender_status=False) | Q(recipient_status=False)),
            'all_documents': all_documents,
            'finish': Document.objects.filter(Q(sender_status=True)),
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
    
    all_documents = Document.objects.filter(Q(recipient=request.user) | Q(sender=request.user))
    all_documents = filter_all_documents(request, all_documents)

    types = DocumentType.objects.all().exclude(type_document='OTKAZ')

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
        'title': 'Мои Документы',
        'form': form,
        'doc_title': 'Отправить на подпись',
        'all_users': CustomUser.objects.all().count(),
        'all_doctors': CustomUser.objects.filter(type='DO').count(),
        'all_clients': CustomUser.objects.filter(type='CL').count(),
        'all_active_documents': Document.objects.filter(
        Q(sender=request.user) | Q(recipient=request.user)).filter(
        Q(sender_status=False) | Q(recipient_status=False)),
        'all_documents': all_documents,
        'types': types,
        }
    if request.user.type == 'CL':
        return render(request, 'documents/clmydocuments.html', context=context)
    else:
        return render(request, 'documents/mydocuments.html', context=context)


@login_required
def show_my_sign_documents(request):
    context = {
        'title': 'Не подписанные',
        'all_users': CustomUser.objects.all().count(),
        'all_doctors': CustomUser.objects.filter(type='DO').count(),
        'all_clients': CustomUser.objects.filter(type='CL').count(),
        'all_sign_documents': Document.objects.filter(
            Q(sender=request.user) | Q(recipient=request.user)).filter(
            Q(sender_status=False, sender=request.user) | Q(recipient_status=False, recipient=request.user)),
    }
    if request.user.type == 'CL':
        return render(request, 'documents/clsign.html', context)
    else:
        return render(request, 'documents/mysign.html', context)


@login_required
def show_my_finish_documents(request):
    context ={
        'title': 'Подписанные',
        'all_users': CustomUser.objects.all().count(),
        'all_doctors': CustomUser.objects.filter(type='DO').count(),
        'all_clients': CustomUser.objects.filter(type='CL').count(),
        'all_finish_documents': Document.objects.filter(
            Q(sender=request.user) | Q(recipient=request.user)).filter(Q(sender_status=True, sender=request.user) | Q(recipient_status=True, recipient=request.user))
    }

    if request.user.type == 'CL':
        return render(request, 'documents/clfinish.html', context)
    else:
        return render(request, 'documents/myfinish.html', context)


@login_required
def show_sign_documents(request):
    context = {
        'title': 'Не подписанные',
        'all_users': CustomUser.objects.all().count(),
        'all_doctors': CustomUser.objects.filter(type='DO').count(),
        'all_clients': CustomUser.objects.filter(type='CL').count(),
        'all_sign_documents': Document.objects.filter(
            Q(sender=request.user) | Q(recipient=request.user)).filter(
            Q(sender_status=False, sender=request.user) | Q(recipient_status=False, recipient=request.user)),
    }
    return render(request, 'documents/sign.html', context)


@login_required
def show_finish_documents(request):
    context ={
        'title': 'Подписанные',
        'all_users': CustomUser.objects.all().count(),
        'all_doctors': CustomUser.objects.filter(type='DO').count(),
        'all_clients': CustomUser.objects.filter(type='CL').count(),
        'all_finish_documents': Document.objects.filter(
            Q(sender=request.user) | Q(recipient=request.user)).filter(Q(sender_status=True, sender=request.user) | Q(recipient_status=True, recipient=request.user))
    }
    return render(request, 'documents/finish.html', context)


# def sign_document(request, pk):
#     document = Document.objects.get(pk=pk)
#     if request.user.type == 'CL':
#         document.recipient_status = True
#         document.save()
#         return HttpResponseRedirect(reverse('index'))
#     else:
#         document.sender_status = True
#         document.save()
#         return HttpResponseRedirect(redirect('index'))


# def sign_document_finish(request, pk):
#     document = Document.objects.get(pk=pk)
#     if request.user.type == 'CL':
#         document.recipient_status = True
#         document.save()
#         return redirect('sign')
#     else:
#         document.sender_status = True
#         document.save()
#         return redirect('sign')


def send_code(request):
    code = random.randrange(1000, 9999)
    request.session['code'] = code
    phone = request.user.phone.replace('+', '')
    # send_code_to_phone(phone, code)
    return JsonResponse({'':''})


def check_code(request):
    code_entered = int(request.GET.get('code'))
    code_sent = request.session['code']
    print(code_entered, type(code_entered), code_sent, type(code_sent))
    pk = request.GET.get('pk')
    if code_entered == code_sent:
        document = Document.objects.get(pk=pk)
        if request.user.type == 'CL':
            document.recipient_status = True
            document.save()
        else:
            document.sender_status = True
            document.save()
  
        create_signature(document)
  
        
        media_root = settings.MEDIA_ROOT

        watermark = media_root + "/signature.pdf"
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

            
        result = {'reload': 'y'} # used on the front as a sign to reload page
        return JsonResponse(result)
    result = {'code': ''}
    return JsonResponse(result)


