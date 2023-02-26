from django.contrib import admin
from ..models.models_shopping_cart import *

admin.site.register(ShoppingCart)
admin.site.register(ShoppingCartItem)