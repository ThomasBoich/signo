
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, redirect

# Create your views here.
from documents.models import Document
from forms import SendDocumentForm
from users.models import CustomUser
from .services import *


@login_required
def show_documents(request):
    if request.user.type == 'CL':
        return redirect('index')
    else:    
        search_name = request.GET.get('search')
        period = request.GET.get('period')
        
        all_documents = filter_by_name(search_name)
        if period:
            start_date, end_date = get_dates(period, all_documents) 
            all_documents = all_documents.filter(send_date__range=[start_date, end_date])

        form = SendDocumentForm(request.POST or None, request.FILES)
        if request.method == 'POST':
            if form.is_valid():
                new_doc = form.save(commit=False)
                new_doc.save()
                return redirect('documents')
        else:
            form = SendDocumentForm()

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
            'finish': Document.objects.filter(Q(sender_status=True))
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
        'all_documents': Document.objects.filter(Q(recipient=request.user) | Q(sender=request.user)),
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


def sign_document(request, pk):
    document = Document.objects.get(pk=pk)
    if request.user.type == 'CL':
        document.recipient_status = True
        document.save()
        return redirect('index')
    else:
        document.sender_status = True
        document.save()
        return redirect('index')


def sign_document_finish(request, pk):
    document = Document.objects.get(pk=pk)
    if request.user.type == 'CL':
        document.recipient_status = True
        document.save()
        return redirect('sign')
    else:
        document.sender_status = True
        document.save()
        return redirect('sign')