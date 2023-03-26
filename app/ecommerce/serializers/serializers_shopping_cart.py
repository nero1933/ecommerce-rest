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
    item_price = serializers.ReadOnlyField()
    price = serializers.SerializerMethodField()

    class Meta:
        model = ShoppingCartItem
        fields = ['id', 'cart_id', 'product_item_size_quantity', 'quantity', 'item_price', 'price']

    def get_price(self, obj):
        product_item_price = obj.product_item_size_quantity.product_item.price
        price = obj.quantity * product_item_price
        return price

class ShoppingCartItemUpdateSerializer(ShoppingCartItemSerializer):
    product_item_size_quantity = serializers.PrimaryKeyRelatedField(many=False, read_only=True)


class ShoppingCartSerializer(serializers.ModelSerializer):
    shopping_cart_item = ShoppingCartItemSerializer(many=True, read_only=True)

    class Meta:
        model = ShoppingCart
        fields = ['id', 'user', 'shopping_cart_item']
