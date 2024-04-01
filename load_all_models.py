from datetime import datetime
from decimal import Decimal
import json
import os
from pathlib import Path
import django

#  you have to set the correct path to you settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "arrow_rsc.settings")
django.setup()

from django.core.management import call_command

directory = Path('backups', datetime.today().strftime('%d_%m'))

json_files = os.listdir(directory)
for json_file in json_files:
    call_command('loaddata', Path(directory, json_file))