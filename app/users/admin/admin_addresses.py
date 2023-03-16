from django.contrib import admin
from ..models.models_addresses import Address, UserAddress

admin.site.register(Address)
admin.site.register(UserAddress)
