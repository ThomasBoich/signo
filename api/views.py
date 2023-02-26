from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from rest_framework import status
from rest_framework.parsers import FileUploadParser
from django.contrib.auth import authenticate, login
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect

from documents.models import Document
from .serializers import *

from users.models import *


class UploadDocsAPIViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = FileSerializer
    permission_classes = (IsAuthenticated, )
    # parser_classes = [FileUploadParser]

class APILoginView(LoginView):
    
    def get_success_url(self):
        return reverse_lazy('api:file')
    
    def form_valid(self, form):
        login(self.request, form.get_user())
        return HttpResponseRedirect(self.get_success_url())
    
  