from decimal import Decimal
import json
import os
from pathlib import Path
import django

#  you have to set the correct path to you settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "arrow_rsc.settings")
django.setup()

from vacancy.models import Vacancy, Salary, HourlyPaymentOption
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist

def get_obj_from_list(data: list, id: int) -> dict:
    for item in data:
        if item.get('pk') == id:
            return item.get('fields')
        
def load_json(file_path: str) -> list:
    with open(file_path) as f:
        return json.load(f)
    
# vacancies_json = load_json(Path('backups', 'vacancies.json'))
# with transaction.atomic():
#     for vacancy in Vacancy.objects.all():
#         vacancy_json = get_obj_from_list(vacancies_json, vacancy.pk)
#         fields = ['salary_per_hour_fixed', 'salary_per_mounth_fixed', 'salary_per_mounth_max', 'salary_per_mounth_min']
#         for field in fields:
#             if vacancy_json[field]:
#                 try:
#                     salary = Salary.objects.get(currency='PLN', amount=Decimal(vacancy_json[field]))
#                 except ObjectDoesNotExist:
#                     salary = Salary(currency='PLN', amount=Decimal(vacancy_json[field]))
#                     salary.save()
#                 getattr(vacancy, field).add(salary)
#                 vacancy.save()
    