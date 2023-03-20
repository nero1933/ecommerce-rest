from rest_framework import serializers

from ..models.models_orders import Order, OrderItem, ShippingMethod


class OrderCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Order
        fields = ['id', 'user', 'payment_method', 'shipping_address', 'shipping_method']

    def create(self, validated_data):
        return Order.objects.create(order_price=self.context['order_price'], **validated_data)


class OrderItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderItem
        fields = ['id', 'product_item_size_quantity', 'quantity', 'price']


class OrderDetailSerializer(serializers.ModelSerializer):
    order_item = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'payment_method', 'shipping_address', 'shipping_method', 'order_item']
