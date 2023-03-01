from rest_framework import serializers

from ..models.models_shopping_cart import ShoppingCart, ShoppingCartItem
from ..utils.shopping_cart.shopping_cart import ShoppingCartItemUtil


class ShoppingCartItemSerializer(serializers.ModelSerializer, ShoppingCartItemUtil):

    class Meta:
        model = ShoppingCartItem
        fields = ['id', 'quantity', 'cart_id', 'product_item_size_quantity']

    def create(self, validated_data):
        return self.create_or_update_duplicate(
            self,
            self.context['user'],
            ShoppingCart,
            ShoppingCartItem,
            validated_data
        )

    def update(self, instance, validated_data):
        quantity = validated_data.pop('quantity')
        product_item_size_quantity = validated_data.pop('product_item_size_quantity', instance.product_item_size_quantity)

        instance.quantity = self.check_stock_quantity(
            ShoppingCartItem.objects.get(pk=instance.pk),
            product_item_size_quantity,
            quantity,
            create=False,
        )
        instance.product_item_size_quantity = product_item_size_quantity

        return instance


class ShoppingCartSerializer(serializers.ModelSerializer):
    shopping_cart = ShoppingCartItemSerializer(many=True, read_only=True)

    class Meta:
        model = ShoppingCart
        fields = ['id', 'user', 'shopping_cart']