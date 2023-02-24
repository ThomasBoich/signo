from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets
from documents.models import Document
from .serializers import *

from rest_framework.parsers import FileUploadParser
from users.models import *
from rest_framework.decorators import action
from .serializers import FileSerializer, MultipleFileSerializer


class UploadDocsAPIViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = FileSerializer
    # parser_classes = [FileUploadParser]
    
     

    # @action(detail=False, methods=['POST'])
    # def multiple_uploads(self, request, *args, **kwargs):
    #     serializer = MultipleFileSerializer(data=request.data or None)
    #     serializer.is_valid(raise_exception=True)
    #     files = serializer.validated_data.get('files')
    #     print('!! files =', files)
    #     return Response('Success')


# class GetDocToFrontendAPIViewSet(viewsets.ModelViewSet):
    
#     queryset = Document.objects.get(id=96)
#     serializer_class = FileToFrontSerializer

#     print('!', serializer_class)