from ...models import Product
from ...serializers.serializers_products import ProductSerializer


class ProductAPIMixin:
    serializer_class = ProductSerializer

    def get_queryset(self):
        queryset = Product.objects.all()\
            .select_related('brand') \
            .select_related('category') \
            .select_related('style') \
            .prefetch_related('product_item') \
            .prefetch_related('product_item__discount') \
            .prefetch_related('product_item__color') \
            .prefetch_related('product_item__product_item_sizes__size') \
            .prefetch_related('product_item__product_item_image')

        return queryset