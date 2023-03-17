from django.contrib import admin

from ..models.models_orders import Order, OrderItem, ShippingMethod

admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingMethod)
