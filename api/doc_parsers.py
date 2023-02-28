from documents.models import Document, DocumentType
from users.models import CustomUser
import re
from pdfminer.high_level import extract_pages, extract_text



def doc_parser_main(doc_uploader, validated_data):
    doc_name = validated_data['document']._name
    text = extract_text(validated_data['document'].file)
    id_pattern = re.compile(r"[№]\d+")
    uniq_id = id_pattern.findall(text)[0].split('№')[-1]
    if 'Договор_от_имени_администратора' in doc_name:
        return doc_parser_dogovor(text, uniq_id, validated_data)
    elif 'Административная часть карты' in doc_name:
        print('!here')
        return doc_parser_adm_karta(text, uniq_id, doc_uploader, validated_data)




def doc_parser_adm_karta(text, uniq_id, doc_uploader, validated_data):

    fio_pattern = re.compile(r"(Пациент Ф.И.О.)\n*\w*\s\w*\s\w*")
    try:
        fio = fio_pattern.finditer(text).__next__().group(0).split('\n')[-1]
        recipient = CustomUser.objects.get_or_create(
            uniq_id=uniq_id, 
            defaults={
                'email': uniq_id+'@mailll.ru', 
                'last_name': fio.split(' ')[0],
                'first_name': fio.split(' ')[1],
                'patronymic': fio.split(' ')[2],
                })
        if recipient[1]:
            recipient[0].set_password(f'pass{uniq_id}')
            recipient[0].save()
        doc_type = DocumentType.objects.get(type_document='ADMCARD')
        validated_data['recipient'] = recipient[0]
        validated_data['sender'] = doc_uploader
        validated_data['founder'] = doc_uploader
        validated_data['type'] = doc_type
        print(validated_data)
        return validated_data
    except Exception as e: 
        print(e)



def doc_parser_dogovor(text, uniq_id, validated_data):
    pass