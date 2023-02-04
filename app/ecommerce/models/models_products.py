import decimal

from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from rest_framework.reverse import reverse

from ..utils import productitem_choices
# from ..views import ProductAPIView


class Product(models.Model):
    """ Model describes product. """

    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    product_image = models.CharField(max_length=255, blank=True, null=True)
    brand = models.ForeignKey('Brand', related_name='product', on_delete=models.CASCADE, blank=False, null=False)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, blank=False, null=False)
    style = models.ForeignKey('Style', on_delete=models.CASCADE, blank=False, null=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class ProductItem(models.Model):
    """ Model describes specific kind of product. """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__original_discount = self.discount

    # All sizes are located in productitem_choices.py file
    # in Utils folder
    SIZE_CHOICES = productitem_choices.SIZE_CHOICES
    GENDER_CHOICES = productitem_choices.GENDER_CHOICES

    product = models.ForeignKey('Product', related_name='price', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.1), ])
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.1), ], blank=True, null=True)
    SKU = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField()
    gender = models.CharField(max_length=15, choices=GENDER_CHOICES)
    size = models.CharField(max_length=15, choices=SIZE_CHOICES)
    color = models.ForeignKey('Color', on_delete=models.CASCADE)
    discount = models.ForeignKey('Discount', on_delete=models.PROTECT, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)

    __original_discount = None

    def __str__(self):
        return f'{self.product} / Gender: {self.gender} / Size: {self.size}'

    def save(self, *args, **kwargs):
        """ Automatically changes 'discount_price' when new 'discount' if applied.  """
        if self.discount != self.__original_discount:
            try:
                qs = Discount.objects.filter(name=self.discount).values('discount_rate')
                discount_rate = qs[0].get('discount_rate', 0)
                self.discount_price = self.price - (self.price * decimal.Decimal(discount_rate) / 100)
            except (Discount.DoesNotExist, IndexError):
                self.discount_price = self.price

        super(ProductItem, self).save(*args, **kwargs)
        self.__original_discount = self.discount


class Image(models.Model):
    """ Model for storing
     image urls for product items. """

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


# class Size(BaseDescription):
# """ Model contains sizes. """
#     pass


class Color(BaseDescription):
    """ Model contains colors. """
    pass


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
