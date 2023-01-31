from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    description = models.TextField()
    product_image = models.CharField(max_length=255)
    brand = models.ForeignKey('Brand', on_delete=models.CASCADE)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    style = models.ForeignKey('Style', on_delete=models.CASCADE)


class Brand(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)


class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)


class Style(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)


class ProductItem(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    price = models.IntegerField()
    SKU = models.CharField(max_length=255)
    quantity = models.IntegerField()
    product_image = models.CharField(max_length=255)
    size = models.ForeignKey('Size', on_delete=models.CASCADE)
    color = models.ForeignKey('Color', on_delete=models.CASCADE)


class Size(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)


class Color(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
