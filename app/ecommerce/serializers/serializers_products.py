from rest_framework import serializers

from ..models.models_products import *
from ..utils.price_counters import DiscountCalculator


# ----- ProductAPIList --- starts ----------------------------

class ProductItemSizeQuantitySerializer(serializers.ModelSerializer):
    size = serializers.SlugRelatedField(slug_field='name', read_only=True)

    class Meta:
        model = ProductItemSizeQuantity
        fields = ['id', 'size', 'quantity']


class ProductItemSerializer(serializers.ModelSerializer):
    """
    Serializes several fields from 'ProductItem' model
    for displaying them in 'ProductSerializer' serializer.
    """

    discount_price = serializers.SerializerMethodField()
    color = serializers.SlugRelatedField(slug_field='name', read_only=True)
    #sizes = SizeSerializer(read_only=True, many=True)
    productitem_sizes = ProductItemSizeQuantitySerializer(many=True)

    class Meta:

        model = ProductItem
        # fields = '__all__'
        fields = ['id', 'SKU', 'price', 'discount_price', 'color', 'productitem_sizes']

    @staticmethod
    def get_discount_price(obj):
        """
        Returns 'discount_price' field.
        Value is calculated by 'DiscountCalculator' util class.
        """

        return DiscountCalculator.get_discount_price(obj)


class ProductSerializer(serializers.ModelSerializer):
    """
    Displays values from 'Product' model and particular form 'ProductItem' model.
    Values are show in 'ProductAPIList' view.
    """

    product_item = ProductItemSerializer(many=True, read_only=True)
    brand = serializers.SlugRelatedField(slug_field='name', read_only=True)
    category = serializers.SlugRelatedField(slug_field='name', read_only=True)
    style = serializers.SlugRelatedField(slug_field='name', read_only=True)

    class Meta:
        model = Product
#        fields = '__all__'
        fields = ["id", "name", "product_item", "slug", "description", "brand", "category", "style", "gender", "created"]
#        exclude = ('created', )
        depth = 1


# ----- ProductAPIList --- ends ------------------------------


