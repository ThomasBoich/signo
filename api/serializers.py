import re
from pdfminer.high_level import extract_pages, extract_text

from rest_framework import serializers
from rest_framework.response import Response
from documents.models import Document
from users.models import CustomUser

from .doc_parsers import doc_parser_main

class FileSerializer(serializers.ModelSerializer):
    
    def create(self, validated_data):
        doc_uploader = self.context['request'].user
        resp = doc_parser_main(doc_uploader, validated_data)
        if 'sender' in validated_data and 'founder' in validated_data and 'recipient' in validated_data:
            doc = Document.objects.create(**validated_data)
        
            return doc
        raise serializers.ValidationError({**resp})     
        

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