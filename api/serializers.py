import re

from rest_framework import serializers
from pdfminer.high_level import extract_pages, extract_text

from documents.models import Document
from users.models import CustomUser

from .doc_parsers import doc_parser_main

class FileSerializer(serializers.ModelSerializer):
    
    def create(self, validated_data):
        doc_uploader =  self.context['request'].user
        doc_parser_main(doc_uploader, validated_data)
        
        
        return Document.objects.create(**validated_data)

    class Meta():
        model = Document
        fields = ['document']


class MultipleFileSerializer(serializers.Serializer):
    files = serializers.ListField(child=serializers.FileField())


class FileToFrontSerializer(serializers.ModelSerializer):
    class Meta():
        model = Document
        fields = ['document']

    def get_queryset(self):
        doc_id = self.request.query_params.get('pk')
        queryset = Document.objects.filter(id=doc_id)
        return queryset