from rest_framework import serializers

from .serializers_revews import ReviewSerializer
from ..models.models_products import Product, ProductItem, ProductItemSizeQuantity, Image
from ..utils.products.products_price_counters import DiscountCalculator


class ImageSerializer(serializers.ModelSerializer):
    """
    Serializes 'id', 'image_url' and 'description' fields from 'Image' model
    for displaying them in 'ProductItemSerializer' serializer.
    """

    class Meta:
        model = Image
        fields = ['id', 'image_url', 'description', 'main_image']


class ProductItemSizeQuantitySerializer(serializers.ModelSerializer):
    """
    Serializes 'id', 'size' and 'quantity' fields from 'ProductItemSizeQuantity'
    model for displaying them in 'ProductItemSerializer' serializer.
    """

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
    product_item_image = ImageSerializer(many=True, read_only=True)
    product_item_size_quantity =ProductItemSizeQuantitySerializer(many=True, read_only=True)

    class Meta:
        model = ProductItem
        fields = ['id', 'SKU', 'price', 'discount_price', 'color', 'product_item_size_quantity', 'product_item_image']


    @staticmethod
    def get_discount_price(obj):
        """
        Returns 'discount_price' field.
        Value is calculated by 'DiscountCalculator' util class.
        """

        return DiscountCalculator.get_discount_price(obj)


class ProductRetrieveSerializer(serializers.ModelSerializer):
    """
    Displays values from 'Product' model and particular form 'ProductItem' model.
    Values are show in 'ProductAPIList' view.
    """

    brand = serializers.SlugRelatedField(slug_field='name', read_only=True)
    category = serializers.SlugRelatedField(slug_field='name', read_only=True)
    style = serializers.SlugRelatedField(slug_field='name', read_only=True)
    product_item = ProductItemSerializer(many=True, read_only=True)
    #reviews = ReviewSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ["id", "name", "slug", "description", "brand", "category", "style", "gender", "product_item"]


class ProductListSerializer(serializers.ModelSerializer):

    brand = serializers.SlugRelatedField(slug_field='name', read_only=True)
    category = serializers.SlugRelatedField(slug_field='name', read_only=True)
    style = serializers.SlugRelatedField(slug_field='name', read_only=True)
    product_item = ProductItemSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ["id", "name", "slug", "description", "brand", "category", "style", "gender", "product_item"]


