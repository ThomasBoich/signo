from rest_framework import serializers
from documents.models import Document

class FileSerializer(serializers.ModelSerializer):
    
    class Meta():
        model = Document
        fields = ['document']


class MultipleFileSerializer(serializers.Serializer):
    files = serializers.ListField(child=serializers.FileField())