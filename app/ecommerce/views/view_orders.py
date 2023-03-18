from django.shortcuts import redirect
from rest_framework import viewsets, mixins, status
from rest_framework import generics
from rest_framework.generics import GenericAPIView, CreateAPIView, ListCreateAPIView
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

import decimal

from ..models import ProductItem
from ..models.models_orders import Order, OrderItem
from ..models.models_shopping_cart import ShoppingCartItem
from ..serializers.serializers_orders import CreateOrderSerializer


class CreateOrder(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CreateOrderSerializer

    def post(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        order_id = response.data["id"]
        self.cart_to_order(order_id) # create OrderItem instances from ShoppingCartItem instances for current user
        self.get_queryset().delete() # remove all ShoppingCartItem instances for current user
        return response

    def get_serializer_context(self):
        context = super().get_serializer_context()
        print('hi')
        order_price = self.get_order_price()
        context['order_price'] = order_price
        return context

    def get_order_price(self) -> decimal.Decimal:
        price = sum([item.quantity * item.item_price for item in self.get_queryset()])
        return price

    def cart_to_order(self, order_id):
        order = Order.objects.get(pk=order_id)
        OrderItem.objects.bulk_create(
            OrderItem(
                order=order,
                product_item_size_quantity=cart_item.product_item_size_quantity,
                quantity=cart_item.quantity,
                price=cart_item.item_price,
            )
            for cart_item in self.get_queryset()
        )

    def get_queryset(self):
        queryset = ShoppingCartItem.objects.filter(cart__user=self.request.user) \
            .select_related('product_item_size_quantity')\

        return queryset

