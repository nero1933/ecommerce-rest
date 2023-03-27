from rest_framework import serializers

from ..models.models_products import ProductItemSizeQuantity, ProductItem
from ..models.models_shopping_cart import ShoppingCart, ShoppingCartItem
from ..utils.shopping_cart.shopping_cart import ShoppingCartItemUtil


class ShoppingCartItemSerializer(ShoppingCartItemUtil, serializers.ModelSerializer):
    product_item_size_quantity = serializers.PrimaryKeyRelatedField(
        queryset=ProductItemSizeQuantity.objects.all()
        .select_related('product_item',
                        'product_item__product',
                        'product_item__color'),
    )
    item_price = serializers.SerializerMethodField()
    discount_price = serializers.SerializerMethodField()

    class Meta:
        model = ShoppingCartItem
        fields = ['id', 'cart_id', 'product_item_size_quantity', 'quantity', 'item_price', 'discount_price']

    def get_item_price(self, obj):
        return obj.product_item_size_quantity.product_item.item_price * obj.quantity

    def get_discount_price(self, obj):
        product_item_price = obj.product_item_size_quantity.product_item.get_price()
        price = obj.quantity * product_item_price
        return round(price, 2)


class ShoppingCartItemUpdateSerializer(ShoppingCartItemSerializer):
    product_item_size_quantity = serializers.PrimaryKeyRelatedField(many=False, read_only=True)


class ShoppingCartSerializer(serializers.ModelSerializer):
    shopping_cart_item = ShoppingCartItemSerializer(many=True, read_only=True)

    class Meta:
        model = ShoppingCart
        fields = ['id', 'user', 'shopping_cart_item']
