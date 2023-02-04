from django.db.models import Min
from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField

from ..models.models_products import *


class ProductPriceField(serializers.ModelSerializer):
    class Meta:
        model = ProductItem
        fields = ['price', 'discount_price']


class ProductSerializer(serializers.ModelSerializer):
    price = ProductPriceField(many=True, read_only=True)


    class Meta:
        model = Product
        fields = '__all__'
#        fields = ["id", "name", "price", "slug", "description", "product_image", "brand", "category", "style", "created"]
#        exclude = ('created', )
        depth = 1


