class ShoppingCartItemUtil:
    """  """

    # @classmethod
    def create_or_update_duplicate(
            self,
            serializer,
            user,
            shopping_cart,
            shopping_cart_item,
            validated_data):

        """
        Method checks if a created (added in the shopping cart) product
        already exists. If so, then update quantity of an existing object,
        if no, create an object.
        """

        # serializer = self
        # user = current user instance
        # shopping_cart = shopping cart class
        # shopping_cart_item = shopping cart item class
        # validated_data = validated data

        cart = shopping_cart.objects.get(user=user)
        cart_items = shopping_cart_item.objects.filter(cart=cart).select_related('product_item_size_quantity')

        product_item_size_quantity = validated_data.pop('product_item_size_quantity')
        quantity = validated_data.pop('quantity')

        for item in cart_items:
            if product_item_size_quantity == item.product_item_size_quantity: # If product is in cart
                item.quantity = self.check_stock_quantity(item, product_item_size_quantity, quantity, create=False)
                return serializer.update(item, item.__dict__)

        quantity = self.check_stock_quantity(None, product_item_size_quantity, quantity, create=True)
        return shopping_cart_item.objects.create(
            cart=cart,
            product_item_size_quantity=product_item_size_quantity,
            quantity=quantity,
            **validated_data
        )

    @staticmethod
    def check_stock_quantity(shopping_cart_item, product_item_size_quantity, quantity, create=True) -> int:
        """"""

        if create or quantity <= shopping_cart_item.quantity:
            total_quantity = quantity
        else:
            total_quantity = shopping_cart_item.quantity + quantity

        stock_quantity = product_item_size_quantity.quantity

        if stock_quantity >= total_quantity:
            return total_quantity

        return stock_quantity
