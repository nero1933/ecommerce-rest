from django.db import models
from django.core.validators import MinValueValidator


class Order(models.Model):

    ORDER_STATUS_CHOICES = (
        (1, 'New'),
        (2, 'In progress'),
        (3, 'Shipped'),
        (4, 'Done'),
    )

    PAYMENT_METHODS = (
        (1, 'Cash on delivery'),
        (2, 'Transfer to card'),
        (3, 'Bank transfer'),
    )

    user = models.ForeignKey('users.UserProfile', on_delete=models.PROTECT)
    order_date = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=16, choices=PAYMENT_METHODS, default=1)
    shipping_address = models.ForeignKey('users.Address', on_delete=models.PROTECT)
    shipping_method = models.ForeignKey('ShippingMethod', on_delete=models.PROTECT)
    order_price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.1), ])
    order_status = models.CharField(max_length=15, choices=ORDER_STATUS_CHOICES, default=1)

    def __str__(self):
        return f"{self.user}'s order / {self.order_date}"


class OrderItem(models.Model):
    order = models.ForeignKey('Order', on_delete=models.CASCADE)
    product_item_size_quantity = models.ForeignKey('ProductItemSizeQuantity', on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1), ])
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.1), ])


class ShippingMethod(models.Model):
    delivery_company_name = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.delivery_company_name}'
