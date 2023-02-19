from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveAPIView
from django_filters.rest_framework import DjangoFilterBackend

from ..filters.filters_products import ProductFilter
from ..models.models_products import Product, ProductItem
from ..serializers.serializers_products import ProductSerializer
from ..utils.products.product_mixins import ProductAPIMixin

class ProductAPIList(ProductAPIMixin, ListAPIView):
#    serializer_class = ProductSerializer
    filter_backends = (DjangoFilterBackend, )
    filterset_class = ProductFilter
    # search_fields = ['brand', 'category', 'style']

    # def get_queryset(self):
    #     queryset = Product.objects.all()\
    #         .select_related('brand') \
    #         .select_related('category') \
    #         .select_related('style') \
    #         .prefetch_related('product_item') \
    #         .prefetch_related('product_item__discount') \
    #         .prefetch_related('product_item__color') \
    #         .prefetch_related('product_item__product_item_sizes__size') \
    #         .prefetch_related('product_item__product_item_image')
    #
    #     return queryset


class ProductAPIDetailView(ProductAPIMixin, RetrieveAPIView):
#    serializer_class = ProductSerializer
    lookup_field = 'slug'

    # def get_queryset(self):
    #     queryset = Product.objects.all()\
    #         .select_related('brand') \
    #         .select_related('category') \
    #         .select_related('style') \
    #         .prefetch_related('product_item') \
    #         .prefetch_related('product_item__discount') \
    #         .prefetch_related('product_item__color') \
    #         .prefetch_related('product_item__product_item_sizes__size')
    #
    #     return queryset
