from documents.models import Document, DocumentType
from users.models import CustomUser
import re
from pdfminer.high_level import extract_pages, extract_text



def doc_parser_main(doc_uploader, validated_data):
    doc_name = validated_data['document']._name
    text = extract_text(validated_data['document'].file)
    id_pattern = re.compile(r"[№]\d+")
    uniq_id = id_pattern.findall(text)[0].split('№')[1]
    # try:
    #     client = CustomUser.objects.get(uniq_id=uniq_id, type='CL')
    # except Exception as e:
    #     error = {'error': 'Сначала создайте клиента с номером ' + uniq_id}
    #     return error
    
    # получаем клиента для всех доков кроме договора. В договоре ему присваивается номер. 
    try:
        client = CustomUser.objects.get(uniq_id=uniq_id, type='CL')
    except:
        pass

    if 'Договор' in doc_name:
        return doc_parser_dogovor(text, uniq_id, doc_uploader, validated_data)
    elif 'Амбулаторная карта' in doc_name:
        return doc_parser_adm_karta(text, client, doc_uploader, validated_data)
    elif 'ИДС' in doc_name or 'Отказ от гарантий' in doc_name:
        return doc_parser_ids(text, client, doc_uploader, validated_data)
    elif 'Отказ от медицинского вмешательства' in doc_name:
        return doc_parser_otkaz(text, client, doc_uploader, validated_data)
    elif 'Согласие о лечении без гарантий' in doc_name:
        return doc_parser_soglasie_bez_garantiy(text, client, doc_uploader, validated_data)
    elif 'Уведомление потребителя' in doc_name:
        return doc_parser_uvedomlenie_potrebitelya(text, client, doc_uploader, validated_data)
    elif 'Медицинская карта' in doc_name:
        return doc_parser_med_karta(text, client, doc_uploader, validated_data)
    elif 'Рекомендации стоматолога' in doc_name:
        return doc_parser_dentist_recommendations(text, client, doc_uploader, validated_data)
    elif 'План лечения' in doc_name:
        return doc_parser_plan(text, client, doc_uploader, validated_data)
    elif 'Справка' in doc_name:
        return doc_parser_spravka(text, client, doc_uploader, validated_data)
    elif 'Дневник' in doc_name:
        return doc_parser_dnevnik(text, client, doc_uploader, validated_data)
    else:
        error = {'error': 'Неверное название файла'}
        return error


def get_doctor(text):
    doctor_name_pattern = re.compile(r'\w*\s\w\.\w.')
    doctor_full_name = doctor_name_pattern.findall(text)[-1]
    doctor_last_name = doctor_full_name.split(' ')[0]
    doctor_first_name = doctor_full_name.split(' ')[1].split('.')[0]
    doctor_patronymic = doctor_full_name.split(' ')[1].split('.')[1]

    try:
        doctor = CustomUser.objects.get(
            last_name=doctor_last_name,
            first_name__startswith=doctor_first_name,
            patronymic__startswith=doctor_patronymic,
            type='DO'
            )
        return doctor
    except Exception as e:
        return {'error': 'доктор не существует или найдено несколько с одинаковыми инициалами'}


def get_doctor_type_2(text):
    try:
        doctor_name_pattern = re.compile(r'\s*\w*\s\w{1}.\w{1}')
        doctor_full_name = doctor_name_pattern.findall(text)[-1].strip()
        doctor_last_name = doctor_full_name.split(' ')[0]
        doctor_first_name = doctor_full_name.split(' ')[1].split('.')[0]
        doctor_patronymic = doctor_full_name.split(' ')[1].split('.')[1]
        doctor = CustomUser.objects.get(
            last_name=doctor_last_name, 
            first_name__istartswith=doctor_first_name, 
            patronymic__istartswith=doctor_patronymic,
            type='DO',
            )
        return doctor
    except Exception as e:
        return {'error': 'доктор не существует или найдено несколько с одинаковыми инициалами'}
    

def doc_parser_dogovor(text, uniq_id, doc_uploader, validated_data):

    try:
        client_name_patter = re.compile(r'ЗАКАЗЧИК:\s\w*\s\w*\s\w*')
        client_full_name = client_name_patter.findall(text)[0].split('\n')[1].split(' ')
        client_last_name = client_full_name[0]
        client_first_name = client_full_name[1]
        client_patronymic = client_full_name[2]
        client = CustomUser.objects.get(
            last_name=client_last_name,
            first_name=client_first_name,
            patronymic=client_patronymic,
            type='CL'
        )
        client.uniq_id = uniq_id
        client.save()
    except:
        error = {'error': 'Клиент ' + ' '.join(client_full_name) + ' не найден'}
        return error

    doc_type = DocumentType.objects.get(type_document='DOGOVOR')
    validated_data['recipient'] = client
    validated_data['sender'] = doc_uploader
    validated_data['founder'] = doc_uploader
    validated_data['type'] = doc_type
    return validated_data


def doc_parser_adm_karta(text, client, doc_uploader, validated_data):

    doc_type = DocumentType.objects.get(type_document='ADMCARD')
    validated_data['recipient'] = client
    validated_data['sender'] = doc_uploader
    validated_data['founder'] = doc_uploader
    validated_data['type'] = doc_type
    return validated_data


def doc_parser_ids(text, client, doc_uploader, validated_data):
    
    doc_type = DocumentType.objects.get(type_document='IDS')
    doctor = get_doctor(text)

    validated_data['recipient'] = client
    validated_data['sender'] = doctor
    validated_data['founder'] = doc_uploader
    validated_data['type'] = doc_type
    return validated_data


def doc_parser_otkaz(text, client, doc_uploader, validated_data):
    
    doc_type = DocumentType.objects.get(type_document='OTKAZ_OT_MED')
    doctor = get_doctor(text)

    validated_data['recipient'] = client
    validated_data['sender'] = doctor
    validated_data['founder'] = doc_uploader
    validated_data['type'] = doc_type
    return validated_data


def doc_parser_soglasie_bez_garantiy(text, client, doc_uploader, validated_data):
    
    doc_type = DocumentType.objects.get(type_document='LECHENIE_BEZ_GARANTIY')
    doctor = get_doctor_type_2(text)

    validated_data['recipient'] = client
    validated_data['sender'] = doctor
    validated_data['founder'] = doc_uploader
    validated_data['type'] = doc_type
    return validated_data


def doc_parser_uvedomlenie_potrebitelya(text, client, doc_uploader, validated_data):

    doc_type = DocumentType.objects.get(type_document='UVEDOMLENIE')
    doctor = get_doctor_type_2(text)

    validated_data['recipient'] = client
    validated_data['sender'] = doctor
    validated_data['founder'] = doc_uploader
    validated_data['type'] = doc_type
    return validated_data


def doc_parser_med_karta(text, client, doc_uploader, validated_data):

    doc_type = DocumentType.objects.get(type_document='MEDCARD')

    validated_data['recipient'] = client
    validated_data['sender'] = doc_uploader
    validated_data['founder'] = doc_uploader
    validated_data['type'] = doc_type
    return validated_data



def doc_parser_dentist_recommendations(text, client, doc_uploader, validated_data):

    doc_type = DocumentType.objects.get(type_document='RECOMEND')
    
    doctor_name_pattern = re.compile(r'Подпись врача\s*\w*\s\w{1}.\w{1}.')
    doctor_full_name = doctor_name_pattern.findall(text)[0].split('\n')[-1]
    doctor_last_name = doctor_full_name.split(' ')[0]
    doctor_first_name = doctor_full_name.split(' ')[1].split('.')[0]
    doctor_patronymic = doctor_full_name.split(' ')[1].split('.')[1]
    doctor = CustomUser.objects.get(
        last_name=doctor_last_name, 
        first_name__istartswith=doctor_first_name, 
        patronymic__istartswith=doctor_patronymic,
        type='DO',
        )

    validated_data['recipient'] = client
    validated_data['sender'] = doctor
    validated_data['founder'] = doc_uploader
    validated_data['type'] = doc_type
    return validated_data


def doc_parser_plan(text, client, doc_uploader, validated_data):
        
    doc_type = DocumentType.objects.get(type_document='PLAN')

    doctor_name_pattern = re.compile(r'ФИО доктора:\s*\w*\s*\w*\s*\w*')
    doctor_full_name = doctor_name_pattern.findall(text)[0].split(':')[-1].strip().split(' ')
    doctor_last_name = doctor_full_name[0]
    doctor_first_name = doctor_full_name[1]
    doctor_patronymic = doctor_full_name[2]

    doctor = CustomUser.objects.get(
        last_name=doctor_full_name[0], 
        first_name=doctor_full_name[1], 
        patronymic=doctor_full_name[2],
        type='DO',
        )
    
    validated_data['recipient'] = client
    validated_data['sender'] = doctor
    validated_data['founder'] = doc_uploader
    validated_data['type'] = doc_type
    return validated_data


def doc_parser_spravka(text, client, doc_uploader, validated_data):
    
    doc_type = DocumentType.objects.get(type_document='RENT')

    admin_name_pattern = re.compile(r'Фамилия, имя, отчество лица, выдавшего справку\s*\w*\s+\w\.+\w\.+')
    admin_full_name = admin_name_pattern.findall(text)[0].split('\n')[-1].strip()
    admin_last_name = admin_full_name.split(' ')[0]
    admin_first_name = admin_full_name.split(' ')[1].split('.')[0]
    admin_patronymic = admin_full_name.split(' ')[1].split('.')[1]
    admin = CustomUser.objects.get(
        last_name=admin_last_name, 
        first_name__istartswith=admin_first_name, 
        patronymic__istartswith=admin_patronymic,
        type='AD',
    )
    validated_data['recipient'] = client
    validated_data['sender'] = admin
    validated_data['founder'] = doc_uploader
    validated_data['type'] = doc_type
    return validated_data


def doc_parser_dnevnik(text, client, doc_uploader, validated_data):
    doc_type = DocumentType.objects.get(type_document='DNEVNIK')

    doctor_name_pattern = re.compile(r'Врач Ф.И.О.\s*\w*\s\w.\w.')
    doctor_full_name = doctor_name_pattern.findall(text)[0].strip().split(' ')[2:]
    doctor_last_name = doctor_full_name[0]
    doctor_first_name = doctor_full_name[1].split('.')[0]
    doctor_patronymic = doctor_full_name[1].split('.')[1]
    doctor = CustomUser.objects.get(
        last_name=doctor_last_name, 
        first_name__istartswith=doctor_first_name, 
        patronymic__istartswith=doctor_patronymic,
        type='DO',
    )
    validated_data['recipient'] = client
    validated_data['sender'] = doctor
    validated_data['founder'] = doctor
    validated_data['type'] = doc_type
    return validated_data