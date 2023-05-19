import uuid

from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers

from ecommerce.models import ShoppingCart, ShoppingCartItem, ProductItemSizeQuantity


class ShoppingCartItemSerializerUtil:
    """
    Util class which redefines 'create' and 'update' methods.
    Methods checks max available quantity.
    """

    @staticmethod
    def _check_quantity(product_item_size_quantity: ProductItemSizeQuantity,
                        quantity: int
                        ):
        """
        :param product_item_size_quantity: ProductItemSizeQuantity's instance
        :param quantity: Quantity of an item in shopping cart
        :return: Quantity
        """
        in_stock_quantity = product_item_size_quantity.quantity
        return quantity if quantity <= in_stock_quantity else in_stock_quantity

    def create(self, validated_data):
        product_item_size_quantity = validated_data.pop('product_item_size_quantity')
        quantity = validated_data.pop('quantity')

        if user := self.context.get('user', None):
            cart = ShoppingCart.objects.get(user=user)
        elif session_id := self.context.get('session_id', None):
            cart = ShoppingCart.objects.get(session_id=session_id)

        cart_items = ShoppingCartItem.objects.filter(cart=cart)\
            .select_related('product_item_size_quantity')

        for item in cart_items:
            if product_item_size_quantity == item.product_item_size_quantity: # If product is in cart
                quantity += item.quantity
                item.delete()

        quantity = self._check_quantity(product_item_size_quantity, quantity)

        # When user tries to order a product which is out of stock
        # 'quantity' will be equal to 0 after 'self._check_quantity()' method
        # will run (if 'quantity' > 'is_stock' than 'quantity' = 'is_stock').
        if not quantity:
            raise serializers.ValidationError("Unable to add an item to shopping cart due to out of stock")

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


class ShoppingCartItemViewUtil:

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            try:
                cart = ShoppingCart.objects.get(session_id=self.request.session['unauth'])
            except ObjectDoesNotExist:
                self.request.session['unauth'] = str(uuid.uuid4())
                cart = ShoppingCart.objects.create(session_id=self.request.session['unauth'])
        else:
            cart = ShoppingCart.objects.get(user=self.request.user)

        return ShoppingCartItem.objects.filter(cart=cart)\
            .select_related('product_item_size_quantity__product_item__discount')
