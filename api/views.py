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
    
    print('!', serializer_class)
    # def put(self, request, filename, format=None):
    #     file = request.data['file']
    #     print('!', file)
    #     file.sender = 1
    #     file.save()
    #     return Response(status=204)

    @action(detail=False, methods=['POST'])
    def multiple_uploads(self, request, *args, **kwargs):
        serializer = MultipleFileSerializer(data=request.data or None)
        serializer.is_valid(raise_exception=True)
        files = serializer.validated_data.get('files')
        print('!! files =', files)
        return Response('Success')