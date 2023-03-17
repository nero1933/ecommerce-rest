from ecommerce.models import ShoppingCart, ShoppingCartItem, ProductItem


class ShoppingCartItemUtil:
    """
    Util class which redefines 'create' and 'update' methods.
    Makes check of max available quantity.
    """

    def create(self, validated_data):
        product_item_size_quantity = validated_data.pop('product_item_size_quantity')
        quantity = validated_data.pop('quantity')

        user = self.context['user']
        cart = ShoppingCart.objects.get(user=user)
        item_price = ProductItem.objects.get(product_item_size_quantity=product_item_size_quantity).price
        cart_items = ShoppingCartItem.objects.filter(cart=cart).select_related('product_item_size_quantity')

        for item in cart_items:
            if product_item_size_quantity == item.product_item_size_quantity: # If product is in cart
                quantity += item.quantity
                item.delete()

        quantity = self._check_quantity(product_item_size_quantity, quantity)

        return ShoppingCartItem.objects.create(
            cart=cart,
            product_item_size_quantity=product_item_size_quantity,
            quantity=quantity,
            item_price=item_price,
            **validated_data
        )

    def update(self, instance, validated_data):
        quantity = validated_data.pop('quantity', instance.quantity)
        product_item_size_quantity = validated_data.pop('product_item_size_quantity', instance.product_item_size_quantity)

        instance.product_item_size_quantity = product_item_size_quantity
        instance.quantity = self._check_quantity(product_item_size_quantity, quantity)

        instance.save()
        return instance

    @staticmethod
    def _check_quantity(product_item_size_quantity, quantity):
        in_stock_quantity = product_item_size_quantity.quantity
        return quantity if quantity <= in_stock_quantity else in_stock_quantity