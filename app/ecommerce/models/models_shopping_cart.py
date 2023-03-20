from django.db import models
from django.core.validators import MinValueValidator


class ShoppingCart(models.Model):
    user = models.OneToOneField('UserProfile', related_name='users', on_delete=models.PROTECT)

    def __str__(self):
        return f'Shopping Cart: {self.user}'


class ShoppingCartItem(models.Model):
    cart = models.ForeignKey('ShoppingCart', related_name='shopping_cart_item', on_delete=models.PROTECT)
    product_item_size_quantity = models.ForeignKey('ProductItemSizeQuantity', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    item_price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.1), ])
