from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, redirect

# Create your views here.
from documents.models import Document, DocumentType
from users.models import CustomUser


@login_required
def index(request):

    if request.user.is_authenticated == False:
        return redirect('login')
    # else:
        # all_documents_type = DocumentType.objects.all().count()
    if request.user.is_authenticated and request.user.type == 'AD':
        all_types = DocumentType.objects.all()
        all_documents = Document.objects.all().count()
        finish = Document.objects.all().filter(Q(sender_status=True) & Q(recipient_status=True)).count()
        contract = DocumentType.objects.filter(document__type__pk=1).count()
        ids = Document.objects.filter(pk=2).count()
        medcard = Document.objects.filter(pk=3).count()
        admcard = Document.objects.filter(pk=4).count()
        rent = Document.objects.filter(pk=5).count()
        plan = Document.objects.filter(pk=6).count()

        # signed_contract = Document.objects.filter(type='Договор').filter(Q(sender_status=True) & Q(recipient_status=True)).count()
        # signed_ids = Document.objects.filter(type='ИДС').count().filter(Q(sender_status=True) & Q(recipient_status=True)).count()
        # signed_medcard = Document.objects.filter(type='Мед карта').filter(Q(sender_status=True) & Q(recipient_status=True)).count()
        # signed_admcard = Document.objects.filter(type='Адм.карта').filter(Q(sender_status=True) & Q(recipient_status=True)).count()
        # signed_rent = Document.objects.filter(type='Справка в налоговую').filter(Q(sender_status=True) & Q(recipient_status=True)).count()
        # signed_plan = Document.objects.filter(type='План лечения').filter(Q(sender_status=True) & Q(recipient_status=True)).count()
        context = {
            'title': 'Главная страница',
            'all_users': CustomUser.objects.all().count(),
            'all_doctors': CustomUser.objects.filter(type='DO').count(),
            'all_clients': CustomUser.objects.filter(type='CL').count(),
            'all_active_documents': Document.objects.filter(Q(sender=request.user) | Q(recipient=request.user)).filter(Q(sender_status=False) | Q(recipient_status=False)),
            # 'all_documents_type': all_documents_type,
            'type': all_types,
            # 'signed_contract': signed_contract,
            # 'signed_ids': signed_ids,
            # 'signed_medcard': signed_medcard,
            # 'signed_admcard': signed_admcard,
            # 'signed_rent': signed_rent,
            # 'signed_plan': signed_plan,
            'all_documents': all_documents,
            'finish': finish,
            'contract': contract,
            'ids': ids,
            'medcard': medcard,
            'admcard': admcard,
            'rent': rent,
            'plan': plan,
        }
        return render(request, 'index/cabinet/ad.html', context)
    #
    if request.user.is_authenticated and request.user.type == 'DI':
        context = {
            'title': 'Главная страница',
            'all_users': CustomUser.objects.all().count(),
            'all_doctors': CustomUser.objects.filter(type='DO').count(),
            'all_clients': CustomUser.objects.filter(type='CL').count(),
            'all_active_documents': Document.objects.filter(Q(sender=request.user) | Q(recipient=request.user)).filter(Q(sender_status=False) | Q(recipient_status=False)),
            'type': DocumentType.objects.all(),
            'all_documents': Document.objects.all().count(),
            'finish': Document.objects.all().filter(Q(sender_status=True) & Q(recipient_status=True)).count(),
            'contract': Document.objects.filter(type__type_document='DOGOVOR').count(),
            'ids': Document.objects.filter(type__type_document='IDS').count(),
            'medcard': Document.objects.filter(type__type_document='MEDCARD').count(),
            'admcard': Document.objects.filter(type__type_document='ADMCARD').count(),
            'rent': Document.objects.filter(type__type_document='RENT').count(),
            'plan': Document.objects.filter(type__type_document='PLAN').count(),
            'medcarddne': Document.objects.filter(type__type_document='DNEVNIK').count(),
        }
        return render(request, 'index/cabinet/di.html', context)
    #

    if request.user.is_authenticated and request.user.type == 'DO':
        all_types = DocumentType.objects.all()

        contract = DocumentType.objects.filter(pk=1).count()
        ids = DocumentType.objects.filter(pk=2).count()
        medcard = DocumentType.objects.filter(pk=3).count()
        admcard = DocumentType.objects.filter(pk=4).count()
        medcarddne = DocumentType.objects.filter(pk=8).count()
        rent = DocumentType.objects.filter(pk=5).count()
        plan = DocumentType.objects.filter(pk=6).count()
        # signed_contract = DocumentType.objects.filter(pk=1).filter(Q(sender_status=True) & Q(recipient_status=True)).count()
        # signed_ids = DocumentType.objects.filter(pk=2).count().filter(Q(sender_status=True) & Q(recipient_status=True)).count()
        # signed_medcard = DocumentType.objects.filter(pk=3).filter(Q(sender_status=True) & Q(recipient_status=True)).count()
        # signed_admcard = DocumentType.objects.filter(pk=4).filter(Q(sender_status=True) & Q(recipient_status=True)).count()
        # signed_rent = DocumentType.objects.filter(pk=5).filter(Q(sender_status=True) & Q(recipient_status=True)).count()
        # signed_plan = DocumentType.objects.filter(pk=6).filter(Q(sender_status=True) & Q(recipient_status=True)).count()

        context = {
            'type': all_types,
            'all_active_documents': Document.objects.filter(Q(sender=request.user) | Q(recipient=request.user)).filter(
                Q(sender_status=False) | Q(recipient_status=False)),
            # 'signed_contract': signed_contract,
            # 'signed_ids': signed_ids,
            # 'signed_medcard': signed_medcard,
            # 'signed_admcard': signed_admcard,
            # 'signed_rent': signed_rent,
            # 'signed_plan': signed_plan,

            'contract': contract,
            'ids': ids,
            'medcard': medcard,
            'admcard': admcard,
            'rent': rent,
            'plan': plan,

        }
        return render(request, 'index/cabinet/do.html', context)

    if request.user.is_authenticated and request.user.type == 'CL':
        context = {
            #
            'all_active_documents': Document.objects.filter(Q(sender=request.user) | Q(recipient=request.user)).filter(Q(sender_status=False) | Q(recipient_status=False)),
            #'all_documents_type': all_documents_type,
        }
        return render(request, 'index/cabinet/cl.html', context)