from rest_framework import serializers

from ..models.models_orders import Order, OrderItem


# class OrderCreateSerializer(serializers.ModelSerializer):
#     user = serializers.HiddenField(default=serializers.CurrentUserDefault())
#
#     class Meta:
#         model = Order
#         fields = ['id', 'user', 'payment_method', 'shipping_address', 'shipping_method']
#
#     def create(self, validated_data):
#         return Order.objects.create(order_price=self.context['order_price'],  **validated_data)


class OrderItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderItem
        fields = ['id', 'product_item_size_quantity', 'quantity', 'price']


class OrderSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    order_item = OrderItemSerializer(many=True, read_only=True)
    order_price = serializers.DecimalField(read_only=True, max_digits=10, decimal_places=2)

    class Meta:
        model = Order
        fields = ['id', 'user', 'payment_method', 'shipping_address', 'shipping_method', 'order_item', 'order_price']

    def create(self, validated_data):
        order_items = []
        for item in self.context['shopping_cart_items']:
            order_items.append(
                OrderItem(product_item_size_quantity=item.product_item_size_quantity,
                          quantity=item.quantity,
                          price=item.product_item_size_quantity.product_item.get_price() * item.quantity,
                          )
            )

        order_price = sum(item.price for item in order_items)
        order = Order.objects.create(order_price=order_price, **validated_data)
        for item in order_items:
            item.order = order

        OrderItem.objects.bulk_create(order_items)
        return order

# class OrderSerializer(serializers.ModelSerializer):
#     order_item = OrderItemSerializer(many=True)
#
#     class Meta:
#         model = Order
#         fields = ['id', 'user', 'payment_method', 'shipping_address', 'shipping_method', 'order_item', 'order_price', 'order_status']
