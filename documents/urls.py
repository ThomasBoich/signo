from django.urls import path

from documents.views import show_documents, mydocuments, show_my_sign_documents, show_my_finish_documents, \
    show_sign_documents, show_finish_documents, show_category, send_code, check_code

urlpatterns = [
    path('alldocuments/', show_documents, name='documents'),
    path('mydocuments/', mydocuments, name='mydocuments'),
    path('mydocuments/signed/', show_my_sign_documents, name='mysign'),
    path('mydocuments/finish/', show_my_finish_documents, name='myfinish'),
    path('finish/', show_finish_documents, name='finish'),
    path('sign/', show_sign_documents, name='sign'),
    path('<int:pk>/', show_category, name='category'),

    path('send_code/', send_code, name='send_code'),
    path('check_code/', check_code, name='check_code')

]