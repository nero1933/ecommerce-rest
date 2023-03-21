from rest_framework import serializers

from ..models import Product, ProductItemSizeQuantity, OrderItem
from ..models.models_reviews import Review


class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Review
        fields = ('user', 'rating_value', 'comment')


class ReviewCreateSerializer(ReviewSerializer):
    def create(self, validated_data):
        order_item = OrderItem.objects\
            .select_related('product_item_size_quantity')\
            .get(pk=self.context['ordered_item_id'])

        pisq = ProductItemSizeQuantity.objects\
            .select_related('product_item', 'product_item__product')\
            .get(pk=order_item.product_item_size_quantity.pk)

        return Review.objects.create(product=pisq.product_item.product, order_item=order_item, **validated_data)