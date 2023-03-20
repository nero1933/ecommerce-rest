"""
Django command to wait for the database to be available.
"""

from django.core.management.base import BaseCommand

from ecommerce.utils.addresses.addresses_country_choices import COUNTRY_CHOICES
from users.models import Country


class Command(BaseCommand):
    """Django command to wait for database."""

    def handle(self, *args, **options):
        for country_name in COUNTRY_CHOICES:
            Country.objects.create(name=country_name[0])

        print('Success')
