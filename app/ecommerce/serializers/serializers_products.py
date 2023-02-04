import decimal

from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField

from ..models.models_products import *


class ProductPriceField(serializers.ModelSerializer):
    """ # """

    discount_price = serializers.SerializerMethodField()

    class Meta:
        model = ProductItem
        fields = ['price', 'discount_price']

    def get_discount_price(self, productitem):
        """ # """

        if not productitem.discount:
            return str(productitem.price)

        discount_rate = productitem.discount.discount_rate
        discount_price = productitem.price - (productitem.price * decimal.Decimal(discount_rate) / 100)
        return str(discount_price)


class ProductSerializer(serializers.ModelSerializer):
    """ # """

    price = ProductPriceField(many=True, read_only=True)

    class Meta:
        model = Product
        fields = '__all__'
#        fields = ["id", "name", "price", "slug", "description", "product_image", "brand", "category", "style", "created"]
#        exclude = ('created', )
        depth = 1




