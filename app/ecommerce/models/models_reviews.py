from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Review(models.Model):
    user = models.ForeignKey('UserProfile', on_delete=models.PROTECT)
    product = models.ForeignKey('Product', related_name='reviews', on_delete=models.PROTECT)
    order_item = models.ForeignKey('OrderItem', on_delete=models.PROTECT)
    rating_value = models.PositiveSmallIntegerField(validators=(MinValueValidator(0), MaxValueValidator(5)))
    comment = models.TextField()
