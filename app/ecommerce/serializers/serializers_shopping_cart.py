from rest_framework import serializers

from ..models.models_products import ProductItemSizeQuantity
from ..models.models_shopping_cart import ShoppingCart, ShoppingCartItem
from ..utils.shopping_cart.shopping_cart import ShoppingCartItemUtil


class ShoppingCartItemSerializer(ShoppingCartItemUtil, serializers.ModelSerializer):
    product_item_size_quantity = serializers.PrimaryKeyRelatedField(
        queryset=ProductItemSizeQuantity.objects.all()
        .select_related('size',
                        'product_item',
                        'product_item__product',
                        'product_item__color')
    )

    class Meta:
        model = ShoppingCartItem
        fields = ['id', 'cart_id', 'product_item_size_quantity', 'quantity']


class ShoppingCartSerializer(serializers.ModelSerializer):
    shopping_cart_item = ShoppingCartItemSerializer(many=True, read_only=True)

    class Meta:
        model = ShoppingCart
        fields = ['id', 'user', 'shopping_cart_item']
