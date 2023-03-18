from rest_framework import serializers

from users.models.models_addresses import Address, UserAddress
from ..models.models_orders import Order, OrderItem, ShippingMethod
from ..utils.orders.serializers_default import OrdersPriceDefault


class CreateOrderSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    order_price = serializers.HiddenField(default=OrdersPriceDefault())

    class Meta:
        model = Order
        fields = ['id', 'user', 'payment_method', 'shipping_address', 'shipping_method', 'order_price']


class OrderItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderItem
        fields = '__all__'
