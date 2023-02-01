from django.db import models

from .utils.product_size import SIZE_CHOICES


class Product(models.Model):
    """ Model describes product """

    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    description = models.TextField()
    product_image = models.CharField(max_length=255)
    brand = models.ForeignKey('Brand', on_delete=models.CASCADE, blank=False, null=False)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, blank=False, null=False)
    style = models.ForeignKey('Style', on_delete=models.CASCADE, blank=False, null=False)

    def __str__(self):
        return self.name


class ProductItem(models.Model):
    """ Model describes specific kind of product. """

    # All sizes are located in product_size.py file
    SIZE_CHOICES = SIZE_CHOICES

    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    price = models.IntegerField()
    SKU = models.CharField(max_length=255)
    quantity = models.IntegerField()
    product_image = models.CharField(max_length=255)
    size = models.CharField(max_length=15, choices=SIZE_CHOICES)
    color = models.ForeignKey('Color', on_delete=models.CASCADE)


class BaseDescription(models.Model):
    """ Base class for all descriptions such as brand, style etc. """

    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class Category(BaseDescription):
    """ 1 """
    pass


class Brand(BaseDescription):
    """ 1 """
    pass


class Style(BaseDescription):
    """ 1 """
    pass


# class Size(BaseDescription):
#     """ 1 """
#     pass


class Color(BaseDescription):
    """ 1 """
    pass
