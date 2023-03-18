from rest_framework import viewsets, mixins
from rest_framework import generics
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

import decimal

from ..models import ProductItem
from ..models.models_orders import Order, OrderItem
from ..models.models_shopping_cart import ShoppingCartItem
from ..serializers.serializers_orders import CreateOrderSerializer


class CreateOrder(mixins.CreateModelMixin, GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CreateOrderSerializer

    def post(self, request, *args, **kwargs):
        response = self.create(request, *args, **kwargs)
        order_id = response.data["id"]
        self.set_order(order_id)
        if not self.set_shopping_cart_items(self.request.user):
            return Response(status=400)

        self.cart_to_order()
        self.drop_cart()
        return response

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['order_price'] = self.get_order_price()
        return context

    def get_order_price(self) -> decimal.Decimal:
        shopping_cart_items = ShoppingCartItem.objects.filter(cart__user=self.request.user)
        price = sum((item.quantity * item.item_price) for item in shopping_cart_items)
        return price

    def set_order(self, order_id):
        self.order = Order.objects.get(pk=order_id)

    def set_shopping_cart_items(self, user):
        self.shopping_cart_items = ShoppingCartItem.objects.filter(cart__user=user)
        if len(self.shopping_cart_items) > 0:
            return True

        return False

    def cart_to_order(self):
        for cart_item in self.shopping_cart_items:
            OrderItem.objects.create(
                order=self.order,
                product_item_size_quantity=cart_item.product_item_size_quantity,
                quantity=cart_item.quantity,
                price=cart_item.item_price,
            )

    def drop_cart(self):
        for item in self.shopping_cart_items:
            item.delete()

    def get_queryset(self):
        return OrderItem.objects.all()
