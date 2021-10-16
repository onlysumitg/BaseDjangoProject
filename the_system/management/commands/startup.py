# python manage.py loadbankdata "C:\IdeaProjects\the_office\the_office\the_users\ifsc_code_list.pdf"  --settings=the_office.settings.dev

import logging

from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission

GROUPS = ['brick_manufacturer', 'brick_supplier', 'supplier_to_brick_manufacturer', ]
MODELS = ['video', 'article', 'license', 'list', 'page', 'client']
PERMISSIONS = ['view', ]  # For now only view permission by default for all, others include add, delete, change


class Command(BaseCommand):

    def handle(self, *args, **options):
        _create_groups()


def _create_groups():
    for group in GROUPS:
        new_group, created = Group.objects.get_or_create(name=group)
