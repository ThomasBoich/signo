from rest_framework import serializers
from documents.models import Document
from users.models import CustomUser
import re
from pdfminer.high_level import extract_pages, extract_text


class FileSerializer(serializers.ModelSerializer):
    
    def create(self, validated_data):
        text = extract_text(validated_data['document'].file)

        id_pattern = re.compile(r"[№]\d+")
        fio_pattern = re.compile(r"(Пациент Ф.И.О.)\n*\w*\s\w*\s\w*")
        id = id_pattern.findall(text)[0].split('№')[-1]
        try:
            fio = fio_pattern.finditer(text).__next__().group(0).split('\n')[-1]
            print(id, fio)
            user = CustomUser.objects.get_or_create(
                uniq_id=id, 
                defaults={
                    'email': id+'@mailll.ru', 
                    'last_name': fio.split(' ')[0],
                    'first_name': fio.split(' ')[1],
                    'patronymic': fio.split(' ')[2],
                    })
            if user[1]:
                user[0].set_password(f'pass{id}')
                user[0].save()
            validated_data['recipient'] = user[0]
        except:
            pass
        
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