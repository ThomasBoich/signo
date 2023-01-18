from django.urls import path

from documents.views import show_documents, mydocuments, \
    show_category, send_code, delete_document, sign_document

urlpatterns = [
    path('alldocuments/', show_documents, name='documents'),
    path('mydocuments/', mydocuments, name='mydocuments'),
   
    path('<int:pk>/', show_category, name='category'),

    path('send_code/', send_code, name='send_code'),
    path('sign_document/', sign_document, name='sign_document'),
    path('delete_document/', delete_document, name='delete_document')


]