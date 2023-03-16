from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

class Order(models.Model):
    NEW = 1
    IN_PROGRESS = 2
    SHIPPED = 3
    DONE = 4

    ORDER_STATUS_CHOICES = (
        (NEW, 'New'),
        (IN_PROGRESS, 'In progress'),
        (SHIPPED, 'Shipped'),
        (DONE, 'Done'),
    )

    user = models.ForeignKey('users.UserProfile', on_delete=models.PROTECT)
    order_date = models.DateTimeField(auto_now_add=True)
    payment_method = models.ForeignKey('users.PaymentMethod', on_delete=models.PROTECT)
    shipping_address = models.ForeignKey('users.Address', on_delete=models.PROTECT)
    shipping_method = models.ForeignKey('ShippingMethod', on_delete=models.PROTECT)
    order_price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.1), ])
    order_status = models.CharField(max_length=15, choices=ORDER_STATUS_CHOICES, default=NEW)


class OrderItem(models.Model):
    order = models.ForeignKey('Order', on_delete=models.CASCADE)
    product_item_size_quantity = models.ForeignKey('ProductItemSizeQuantity', on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1), ])
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.1), ])


class ShippingMethod(models.Model):
    delivery_company_name = models.CharField(max_length=100)
