from django.contrib import admin

from ..models.models_orders import Order, OrderItem

admin.site.register(Order)
admin.site.register(OrderItem)


# class OrderAdmin(admin.)