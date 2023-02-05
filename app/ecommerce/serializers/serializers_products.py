import decimal

from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField

from ..models.models_products import *


class ProductItemField(serializers.ModelSerializer):
    """ # """

    discount_price = serializers.SerializerMethodField()

    class Meta:
        model = ProductItem
        fields = ['id', 'price', 'discount_price']

    def get_discount_price(self, productitem):
        """ # """

        if not productitem.discount:
            return str(productitem.price)

        # obj = productitem.select_related('Discount')
        # discount_rate = obj.discount_rate
        print(self.data)
        discount_rate = productitem.discount.discount_rate
        discount_price = productitem.price - (productitem.price * decimal.Decimal(discount_rate) / 100)
        return str(discount_price)


class ProductSerializer(serializers.ModelSerializer):
    """ # """

    product_item = ProductItemField(many=True, read_only=True)

    class Meta:
        model = Product
#        fields = '__all__'
        fields = ["id", "name", "product_item", "slug", "description", "brand", "category", "style", "created"]
#        exclude = ('created', )
        depth = 1




