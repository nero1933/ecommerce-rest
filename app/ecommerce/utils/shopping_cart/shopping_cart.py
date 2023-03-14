from ecommerce.models import ShoppingCart, ShoppingCartItem


class ShoppingCartItemUtil:
    """
    Util class which redefines 'create' and 'update' methods.
    Makes check of max available quantity.
    """

    # def create(self, validated_data):
    #     """
    #     Creates an object if there is no such an object in the shopping card.
    #     If there is one, updates quantity by adding it to existing obj.
    #     While creating, updating method also checks, if user tries to order
    #     more than is in stock, then quantity is set to quantity in stock.
    #     """
    #
    #     user = self.context['user']
    #     cart = ShoppingCart.objects.get(user=user)
    #     cart_items = ShoppingCartItem.objects.filter(cart=cart).select_related('product_item_size_quantity')
    #
    #     product_item_size_quantity = validated_data.pop('product_item_size_quantity')
    #     quantity = validated_data.pop('quantity')
    #
    #     for item in cart_items:
    #         if product_item_size_quantity == item.product_item_size_quantity: # If product is in cart
    #             item.quantity = self._check_stock_quantity(product_item_size_quantity, quantity, shopping_cart_item=item, create=False)
    #             return self.update(item, item.__dict__)
    #
    #     quantity = self._check_stock_quantity(product_item_size_quantity, quantity, create=True)
    #     return ShoppingCartItem.objects.create(
    #         cart=cart,
    #         product_item_size_quantity=product_item_size_quantity,
    #         quantity=quantity,
    #         **validated_data
    #     )

    def create(self, validated_data):
        user = self.context['user']
        cart = ShoppingCart.objects.get(user=user)
        cart_items = ShoppingCartItem.objects.filter(cart=cart).select_related('product_item_size_quantity')

        product_item_size_quantity = validated_data.pop('product_item_size_quantity')
        quantity = validated_data.pop('quantity')

        for item in cart_items:
            if product_item_size_quantity == item.product_item_size_quantity: # If product is in cart
                quantity += item.quantity
                item.delete()

        # in_stock_quantity = product_item_size_quantity.quantity
        # quantity = quantity if quantity <= in_stock_quantity else in_stock_quantity
        quantity = self._check_quantity(product_item_size_quantity, quantity)

        return ShoppingCartItem.objects.create(
            cart=cart,
            product_item_size_quantity=product_item_size_quantity,
            quantity=quantity,
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


    # @staticmethod
    # def _check_stock_quantity(product_item_size_quantity, quantity, shopping_cart_item=None, create=True) -> int:
    #     """
    #     Method checks, if user tries to order more than is in stock,
    #     then quantity is set to quantity in stock.
    #     """
    #
    #     if create or quantity <= shopping_cart_item.quantity:
    #         total_quantity = quantity
    #     else:
    #         total_quantity = shopping_cart_item.quantity + quantity
    #
    #     stock_quantity = product_item_size_quantity.quantity
    #
    #     if stock_quantity >= total_quantity:
    #         return total_quantity
    #
    #     return stock_quantity
