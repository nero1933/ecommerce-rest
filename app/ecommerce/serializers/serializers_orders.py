from rest_framework import serializers

from ..models.models_orders import Order, OrderItem
from ..utils.orders.serializers_default import OrdersPriceDefault


class CreateOrderSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    order_price = serializers.HiddenField(default=OrdersPriceDefault())

    class Meta:
        model = Order
        fields = ['id', 'user', 'payment_method', 'shipping_address', 'shipping_method', 'order_price']

    def get_order_price(self, obj):
        return self.context['order_price']


class OrderItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderItem
        fields = '__all__'
