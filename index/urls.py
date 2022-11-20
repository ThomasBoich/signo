from django.urls import path

from documents.views import sign_document_finish, sign_document
from index.views import index

urlpatterns = [
    path('', index, name='index'),
    path('sign/<int:pk>', sign_document, name='sign_document'),
]