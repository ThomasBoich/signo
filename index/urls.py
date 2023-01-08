from django.urls import path

# from documents.views import sign_document_finish
from index.views import index, myclients

urlpatterns = [
    path('', index, name='index'),
    # path('sign/<int:pk>', sign_document, name='sign_document'),
    path('myclients/', myclients, name='myclients'),
]