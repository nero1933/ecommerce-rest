from django.contrib import admin
from ..models.models_addresses import Address, Country, UserAddress

admin.site.register(Address)
admin.site.register(Country)
admin.site.register(UserAddress)
