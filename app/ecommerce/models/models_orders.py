from django.db import models
from django.core.validators import MinValueValidator

import enum

class Order(models.Model):

    class OrderStatus(enum.Enum):
        NEW = 1
        IN_PROGRESS = 2
        SHIPPED = 3
        DONE = 4

    class OrderMethods(enum.Enum):
        CASH_ON_DELIVERY = 1
        TRANSFER_TO_THE_CARD = 2
        BANK_TRANSFER = 3

    user = models.ForeignKey('UserProfile', on_delete=models.PROTECT)
    order_date = models.DateTimeField(auto_now_add=True)
    payment_method = models.PositiveSmallIntegerField(choices=[(x.value, x.name) for x in OrderMethods], default=1)
    shipping_address = models.ForeignKey('Address', on_delete=models.PROTECT)
    shipping_method = models.ForeignKey('ShippingMethod', on_delete=models.PROTECT)
    order_price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.1), ])
    order_status = models.PositiveSmallIntegerField(choices=[(x.value, x.name) for x in OrderStatus], default=1)

    def __str__(self):
        return f"{self.user}'s order / {self.order_date}"


class OrderItem(models.Model):
    order = models.ForeignKey('Order', related_name='order_item', on_delete=models.CASCADE)
    product_item_size_quantity = models.ForeignKey('ProductItemSizeQuantity', related_name='ordered_product', on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1), ])
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.1), ])


class ShippingMethod(models.Model):
    delivery_company_name = models.CharField(max_length=100)

    # def __str__(self):
    #     return f'{self.delivery_company_name}'

