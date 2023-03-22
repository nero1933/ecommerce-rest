from django.db import connections
from django.shortcuts import redirect

from rest_framework import viewsets
from rest_framework.reverse import reverse
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated

import decimal

from ..models.models_orders import Order, OrderItem
from ..models.models_shopping_cart import ShoppingCartItem
from ..permissions.permissoins_orders import NotEmptyShoppingCart
from ..serializers.serializers_orders import OrderCreateSerializer, OrderSerializer


class OrderCreateAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated, NotEmptyShoppingCart]
    serializer_class = OrderCreateSerializer

    def post(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        order_id = response.data["id"]
        self._cart_to_order(order_id) # create OrderItem instances from ShoppingCartItem instances for current user
        self.get_queryset().delete() # remove all ShoppingCartItem instances for current user
        return redirect(reverse('orders-detail', kwargs={"pk": order_id}))

    def get_queryset(self):
        """ Queryset contains all users shopping cart items. """

        queryset = ShoppingCartItem.objects.filter(cart__user=self.request.user) \
            .select_related('product_item_size_quantity')

        return queryset

    def get_serializer_context(self):
        """ Passes additional argument 'order_price' to serializer. """

        context = super().get_serializer_context()
        order_price = self._get_order_price()
        context['order_price'] = order_price
        return context

    def _get_order_price(self) -> decimal.Decimal:
        """ Calculates total price of the order. """

        price = sum([item.quantity * item.item_price for item in self.get_queryset()])
        return price

    def _cart_to_order(self, order_id):
        """
        Method retrieves created 'Order' instance and creates 'OrderItem'
        for each of 'ShoppingCartItem' instance in users shopping cart
        """

        order = Order.objects.get(pk=order_id)
        OrderItem.objects.bulk_create(
            OrderItem(
                order=order,
                product_item_size_quantity=cart_item.product_item_size_quantity,
                quantity=cart_item.quantity,
                price=cart_item.item_price * cart_item.quantity, # calculates total price
            )
            for cart_item in self.get_queryset()
        )


class OrderReadOnlyViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated, ]
    lookup_field = 'pk'

    def get_queryset(self):
        queryset = Order.objects.filter(user=self.request.user) \
            .prefetch_related('order_item')

        return queryset