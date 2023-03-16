from rest_framework import viewsets

from django_filters.rest_framework import DjangoFilterBackend

from ..filters.filters_products import ProductFilter
from ..models.models_products import Product
from ..serializers.serializers_products import ProductSerializer


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ProductSerializer
    filter_backends = (DjangoFilterBackend, )
    filterset_class = ProductFilter
    lookup_field = 'slug'

    def get_queryset(self):
        queryset = Product.objects.all()\
            .select_related('brand')\
            .select_related('category')\
            .select_related('style')\
            .prefetch_related('product_item')\
            .prefetch_related('product_item__discount')\
            .prefetch_related('product_item__color') \
            .prefetch_related('product_item__product_item_size_quantity')\
            .prefetch_related('product_item__product_item_image')

        return queryset
