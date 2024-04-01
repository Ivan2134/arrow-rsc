from datetime import datetime
from decimal import Decimal
import json
import os
from pathlib import Path
import django
from django.db import IntegrityError

#  you have to set the correct path to you settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "arrow_rsc.settings")
django.setup()

from info_pages.models import LegalDocument, Team, Partners, Guarantees, AboutUs, ContactInfo, SocialNetwork, PhoneNumber
from vacancy.models import Category, Vacancy, HourlyPaymentOption, Requirement, WorkDuty, InfoLabel, Sex, City, State

def get_obj_from_list(data: list, id: int) -> dict:
    for item in data:
        if item.get('pk') == id:
            return item.get('fields')
        
def load_json(file_path: str) -> list:
    with open(file_path) as f:
        return json.load(f)

directory = Path('backups', datetime.today().strftime('%d_%m'))

def move_data_to_ru_fields():
    # Move data for LegalDocument
    documents = load_json(Path(directory, f'info_pages_{LegalDocument.__name__.lower()}s.json'))
    for document in LegalDocument.objects.all():
        document_old = get_obj_from_list(documents, document.pk)
        document.name = document_old['name']
        document.text = document_old['text']
        document.save()

    documents = load_json(Path(directory, f'info_pages_{Team.__name__.lower()}s.json'))
    for team_member in Team.objects.all():
        document_old = get_obj_from_list(documents, team_member.pk)
        team_member.name = document_old['name']
        team_member.position = document_old['position']
        team_member.save()

    documents = load_json(Path(directory, f'info_pages_{Partners.__name__.lower()}s.json'))
    for partner in Partners.objects.all():
        document_old = get_obj_from_list(documents, partner.pk)
        partner.name = document_old['name']
        partner.save()

    documents = load_json(Path(directory, f'info_pages_{Guarantees.__name__.lower()}s.json'))
    for guarantee in Guarantees.objects.all():
        document_old = get_obj_from_list(documents, guarantee.pk)
        guarantee.title = document_old['title']
        guarantee.description = document_old['description']
        guarantee.save()

    documents = load_json(Path(directory, f'info_pages_{AboutUs.__name__.lower()}s.json'))
    for about_us in AboutUs.objects.all():
        document_old = get_obj_from_list(documents, about_us.pk)
        about_us.title = document_old['title']
        about_us.text = document_old['text']
        about_us.save()

    documents = load_json(Path(directory, f'info_pages_{PhoneNumber.__name__.lower()}s.json'))
    for phone_number in PhoneNumber.objects.all():
        document_old = get_obj_from_list(documents, phone_number.pk)
        phone_number.phone_number = document_old['phone_number']
        phone_number.save()

    documents = load_json(Path(directory, f'vacancy_{Vacancy.__name__.lower()}s.json'))
    for vacancy in Vacancy.objects.all():
        document_old = get_obj_from_list(documents, vacancy.pk)
        vacancy.name = document_old['name']
        vacancy.title = document_old['title']
        vacancy.description = document_old['description']
        vacancy.work_schedule = document_old['work_schedule']
        vacancy.save()

    documents = load_json(Path(directory, f'vacancy_{HourlyPaymentOption.__name__.lower()}s.json'))
    for payment_option in HourlyPaymentOption.objects.all():
        document_old = get_obj_from_list(documents, payment_option.pk)
        payment_option.payment_type = document_old['payment_type']
        payment_option.save()

    documents = load_json(Path(directory, f'vacancy_{Requirement.__name__.lower()}s.json'))
    for requirement in Requirement.objects.all():
        document_old = get_obj_from_list(documents, requirement.pk)
        requirement.description = document_old['description']
        requirement.save()

    documents = load_json(Path(directory, f'vacancy_{WorkDuty.__name__.lower()}s.json'))
    for duty in WorkDuty.objects.all():
        document_old = get_obj_from_list(documents, duty.pk)
        duty.description = document_old['description']
        duty.save()

    documents = load_json(Path(directory, f'vacancy_{InfoLabel.__name__.lower()}s.json'))
    for label in InfoLabel.objects.all():
        document_old = get_obj_from_list(documents, label.pk)
        label.house = document_old['house']
        label.benefits = document_old['benefits']
        label.save()

    documents = load_json(Path(directory, f'vacancy_{Sex.__name__.lower()}s.json'))
    for sex in Sex.objects.all():
        document_old = get_obj_from_list(documents, sex.pk)
        sex.name = document_old['name']
        sex.save()

    documents = load_json(Path(directory, f'vacancy_{City.__name__.lower()}s.json'))
    for city in City.objects.all():
        document_old = get_obj_from_list(documents, city.pk)
        city.name = document_old['name']
        city.save()
        
    documents = load_json(Path(directory, f'vacancy_{Category.__name__.lower()}s.json'))
    for city in Category.objects.all():
        document_old = get_obj_from_list(documents, city.pk)
        city.name = document_old['name']
        city.save()

    documents = load_json(Path(directory, f'vacancy_{State.__name__.lower()}s.json'))
    for state in State.objects.all():
        document_old = get_obj_from_list(documents, state.pk)
        state.name = document_old['name']
        state.save()

if __name__ == "__main__":
    move_data_to_ru_fields()
