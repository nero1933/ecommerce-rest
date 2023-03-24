from rest_framework import serializers

from ..models import OrderItem
from ..models.models_reviews import Review


class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(many=False, read_only=True)

    class Meta:
        model = Review
        fields = ('id', 'user', 'rating_value', 'comment')


class ReviewCreateSerializer(ReviewSerializer):
    def create(self, validated_data):
        product, order_item = self.get_related_objects()
        return Review.objects.create(user=self.context['user'],
                                     product=product,
                                     order_item=order_item,
                                     **validated_data)

    def get_related_objects(self):
        order_item = OrderItem.objects\
            .select_related('product_item_size_quantity__product_item__product')\
            .get(pk=self.context['order_item_id'])
        product = order_item.product_item_size_quantity.product_item.product
        return product, order_item
