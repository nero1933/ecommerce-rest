from django.db import models

from phonenumber_field.modelfields import PhoneNumberField

from ecommerce.utils.addresses.addresses_country_choices import COUNTRY_CHOICES


class UserAddress(models.Model):
    user = models.ForeignKey('UserProfile', on_delete=models.CASCADE)
    address = models.ForeignKey('Address', related_name='address', on_delete=models.CASCADE)
    is_default = models.BooleanField(default=False)

    def __str__(self):
        return f'Address for: {self.user}'


class Address(models.Model):
    name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)
    street = models.CharField(max_length=255)
    unit_number = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=50, choices=COUNTRY_CHOICES, unique=True)
    region = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    post_code = models.PositiveIntegerField()
    phone = PhoneNumberField()

    # def __str__(self):
    #     return f'{self.city}, {self.street}'
