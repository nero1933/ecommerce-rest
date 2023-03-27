from decimal import Decimal

from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from rest_framework.reverse import reverse

from ..utils.products import products_size_choices


class Product(models.Model):
    """ Model describes products. """

    class Meta:
        ordering = ('-date_created',)

    GENDER_CHOICES = [
        ('M', 'Men'),
        ('W', 'Women'),
    ]

    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    brand = models.ForeignKey('Brand', related_name='products', on_delete=models.CASCADE, blank=False, null=False)
    gender = models.CharField(max_length=15, choices=GENDER_CHOICES)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, blank=False, null=False)
    style = models.ForeignKey('Style', on_delete=models.CASCADE, blank=False, null=False)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('products', kwargs={'slug': self.slug})


class ProductItem(models.Model):
    """ Model describes specific kind of products. """

    product = models.ForeignKey('Product', related_name='product_item', on_delete=models.CASCADE)
    SKU = models.CharField(max_length=255)
    item_price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.1), ])
    color = models.ForeignKey('Color', related_name='product_color', on_delete=models.CASCADE)
    discount = models.ForeignKey('Discount', on_delete=models.PROTECT, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.product.name} / Color: {self.color}'

    def get_price(self):
        if not self.discount:
            price = self.item_price
        else:
            price = self.item_price * Decimal((100 - self.discount.discount_rate) / 100)
            price = Decimal(price)

        return price


class BaseDescription(models.Model):
    """ Abstract class for all descriptions such as brand, style etc. """

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


# class Size(models.Model):
#     """ Model contains sizes. """
#
#     SIZE_CHOICES = products_size_choices.SIZE_CHOICES
#
#     name = models.CharField(max_length=15, choices=SIZE_CHOICES, unique=True)
#
#     def __str__(self):
#         return self.name


class Discount(models.Model):
    """ Model contains discounts. """

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    discount_rate = models.PositiveIntegerField(blank=False, null=False, validators=[MaxValueValidator(99.9)])
    is_active = models.BooleanField(default=True)
    start_date = models.DateTimeField(auto_now=False, auto_now_add=False)
    end_date = models.DateTimeField(auto_now=False, auto_now_add=False)

    def __str__(self):
        return self.name


class ProductItemSizeQuantity(models.Model):
    """ Model describes specific kind of products. """

    SIZE_CHOICES = products_size_choices.SIZE_CHOICES

    product_item = models.ForeignKey('ProductItem', on_delete=models.CASCADE, related_name='product_item_size_quantity')
    size = models.CharField(max_length=15, choices=SIZE_CHOICES)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.product_item} / Size: {self.size}'
        #return f'Size: {self.size}'


class Image(models.Model):
    """ Model for storing image urls for products. """

    product_item = models.ForeignKey('ProductItem', related_name='product_item_image', on_delete=models.CASCADE, blank=False, null=False)
    description = models.CharField(max_length=255, blank=True, null=True)
    image_url = models.URLField(max_length=255)
    main_image = models.BooleanField(default=False)

    def __str__(self):
        return f'Image for: {self.product_item}'
