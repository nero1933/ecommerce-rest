# import decimal

from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from rest_framework.reverse import reverse

from ..utils import product_size_choices
# from ..views import ProductAPIView


class Product(models.Model):
    """ Model describes product. """

    GENDER_CHOICES = [
        ('M', 'Men'),
        ('W', 'Women'),
    ]

    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    brand = models.ForeignKey('Brand', related_name='product', on_delete=models.CASCADE, blank=False, null=False)
    gender = models.CharField(max_length=15, choices=GENDER_CHOICES)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, blank=False, null=False)
    style = models.ForeignKey('Style', on_delete=models.CASCADE, blank=False, null=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class ProductItem(models.Model):
    """ Model describes specific kind of product. """

    product = models.ForeignKey('Product', related_name='product_item', on_delete=models.CASCADE)
    product_image = models.ForeignKey('Image', related_name='image', on_delete=models.CASCADE, blank=True, null=True)
    SKU = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.1), ])
    color = models.ForeignKey('Color', on_delete=models.CASCADE)
    discount = models.ForeignKey('Discount', on_delete=models.PROTECT, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.product.name} / Color: {self.color}'


class ProductItemSizeAmount(models.Model):
    """ Model describes specific kind of product. """

    SIZE_CHOICES = product_size_choices.SIZE_CHOICES

    productitem = models.ForeignKey('ProductItem', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    size = models.CharField(max_length=15, choices=SIZE_CHOICES)


class Image(models.Model):
    """ Model for storing image urls for products. """

    product = models.ForeignKey('ProductItem', on_delete=models.CASCADE, blank=False, null=False)
    description = models.TextField(blank=True, null=True)
    product_image = models.CharField(max_length=255)

    def __str__(self):
        return f'Image for: {self.product}'


class BaseDescription(models.Model):
    """ Base class for all descriptions such as brand, style etc. """

    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('products', kwargs={'slug': self.slug})


class Category(BaseDescription):
    """ Model contains categories. """
    pass


class Brand(BaseDescription):
    """ Model contains brands. """
    pass


class Style(BaseDescription):
    """ Model contains styles. """
    pass


class Color(BaseDescription):
    """ Model contains colors. """
    pass


# class Temp(BaseDescription):
#     """ Model contains temp. """
#     pass


class Discount(models.Model):
    """ Model contains discounts. """

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    discount_rate = models.FloatField(blank=False, null=False, validators=[MinValueValidator(0.5), MaxValueValidator(99.9)])
    is_active = models.BooleanField(default=True)
    start_date = models.DateTimeField(auto_now=False, auto_now_add=False)
    end_date = models.DateTimeField(auto_now=False, auto_now_add=False)

    def __str__(self):
        return self.name
