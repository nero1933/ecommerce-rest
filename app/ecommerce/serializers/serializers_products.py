from rest_framework import serializers

from .serializers_revews import ReviewSerializer
from ..models.models_products import Product, ProductItem, ProductItemSizeQuantity, Image


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
    product_item_size_quantity = ProductItemSizeQuantitySerializer(many=True, read_only=True)
    item_price = serializers.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        model = ProductItem
        fields = ['id', 'SKU', 'item_price', 'discount_price', 'color', 'product_item_size_quantity', 'product_item_image']

    def get_discount_price(self, obj):
        """

        """

        return round(obj.get_price(), 2)


class ProductSerializer(serializers.ModelSerializer):

    brand = serializers.SlugRelatedField(slug_field='name', read_only=True)
    category = serializers.SlugRelatedField(slug_field='name', read_only=True)
    style = serializers.SlugRelatedField(slug_field='name', read_only=True)
    product_item = ProductItemSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ["id", "name", "slug", "description", "brand", "category", "style", "gender", "product_item"]


class ProductDetailSerializer(ProductSerializer):
    """
    Displays values from 'Product' model and particular form 'ProductItem' model.
    Values are show in 'ProductAPIList' view.
    """

    reviews = ReviewSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ["id", "name", "slug", "description", "brand", "category", "style", "gender", "product_item", "reviews"]