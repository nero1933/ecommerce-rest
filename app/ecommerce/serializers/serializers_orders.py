from rest_framework import serializers

from ..models.models_orders import Order, OrderItem, ShippingMethod


class CreateOrderSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Order
        fields = ['id', 'user', 'payment_method', 'shipping_address', 'shipping_method']

    def create(self, validated_data):
        return Order.objects.create(order_price=self.context['order_price'], **validated_data)


class OrderItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderItem
        fields = '__all__'
