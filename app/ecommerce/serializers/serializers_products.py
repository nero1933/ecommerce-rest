from rest_framework import serializers

from ..models.models_products import Product, ProductItem, ProductItemSizeQuantity, Image
from ..utils.product.price_counters import DiscountCalculator


class ProductItemSizeQuantitySerializer(serializers.ModelSerializer):
    """
    Serializes 'id', 'size' and 'quantity' fields from 'ProductItemSizeQuantity'
    model for displaying them in 'ProductItemSerializer' serializer.
    """

    size = serializers.SlugRelatedField(slug_field='name', read_only=True)

    class Meta:
        model = ProductItemSizeQuantity
        fields = ['id', 'size', 'quantity']


class ImageSerializer(serializers.ModelSerializer):
    """
    Serializes 'id', 'image_url' and 'description' fields from 'Image' model
    for displaying them in 'ProductItemSerializer' serializer.
    """

    class Meta:
        model = Image
        fields = ['id', 'image_url', 'description', 'main_image']


class ProductItemSerializer(serializers.ModelSerializer):
    """
    Serializes several fields from 'ProductItem' model
    for displaying them in 'ProductSerializer' serializer.
    """

    discount_price = serializers.SerializerMethodField()
    color = serializers.SlugRelatedField(slug_field='name', read_only=True)
    product_item_sizes = ProductItemSizeQuantitySerializer(many=True)
    product_item_image = ImageSerializer(many=True, read_only=True)

    class Meta:

        model = ProductItem
        # fields = '__all__'
        fields = ['id', 'SKU', 'price', 'discount_price', 'color', 'product_item_sizes', 'product_item_image']

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
#        depth = 1
