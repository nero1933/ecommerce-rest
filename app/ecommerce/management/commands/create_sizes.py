from django.core.management.base import BaseCommand

from ...models import Size
from ...utils.products.products_size_choices import SIZE_CHOICES


class Command(BaseCommand):
    """Django command to wait for database."""

    def handle(self, *args, **options):
        for category in SIZE_CHOICES:
            for size in category[1]:
                Size.objects.create(name=size[0])

        print('Success')