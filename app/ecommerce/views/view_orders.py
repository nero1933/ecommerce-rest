from rest_framework import viewsets, mixins
from rest_framework import generics
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from ..models import ProductItem
from ..models.models_orders import Order, OrderItem
from ..models.models_shopping_cart import ShoppingCartItem
from ..serializers.serializers_orders import CreateOrderSerializer


class CreateOrder(mixins.CreateModelMixin, GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CreateOrderSerializer

    # def post(self, request):
    #
    #
    #     queryset_cart = ShoppingCartItem.objects.filter(cart__user=self.request.user) \
    #                         .select_related('cart')
    #     print(queryset_cart)
    #
    #     return Response('ok')

    # def cart_to_order(self, cart_item):
    #     pass
    def post(self, request):
        print(self.get_order_price())
        return Response('200 OK')

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['price'] = 1 #
        return context

    def get_order_price(self):
        shopping_cart_items = ShoppingCartItem.objects.filter(cart__user=self.request.user) \
                    .select_related('cart')

        price = sum((item.quantity * item.item_price) for item in shopping_cart_items)
        return price




