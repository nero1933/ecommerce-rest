from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveAPIView
from django_filters.rest_framework import DjangoFilterBackend

from ..filters.filters_products import ProductFilter
from ..models.models_products import Product, ProductItem
from ..serializers.serializers_products import ProductSerializer


class ProductAPIList(ListAPIView):
    # queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = (DjangoFilterBackend, )
    filterset_class = ProductFilter
    # search_fields = ['brand', 'category', 'style']

    def get_queryset(self):
        queryset = Product.objects.all()\
            .select_related('brand')\
            .select_related('category')\
            .select_related('style')\
            .prefetch_related('product_item')\
            .prefetch_related('product_item__discount')\
            .prefetch_related('product_item__color') \
            .prefetch_related('product_item__sizes') \

        return queryset

    # def get_serializer_context(self):
    #     context = super().get_serializer_context()
    #     # context["color"] = self.get_queryset().filter('color')
    #     print(self.get_queryset().get('color'))
    #     # context["query_params"] = self.request.query_params
    #     return context


# class ProductAPIView(DetailAPIView):
#     # queryset = Product.objects.all()
#     serializer_class = ProductSerializer
#     filter_backends = (DjangoFilterBackend, )
#     filterset_class = ProductFilter
#     # search_fields = ['brand', 'category', 'style']
#
#     def get_queryset(self):
#         queryset = Product.objects.all()\
#             .select_related('brand')\
#             .select_related('category')\
#             .select_related('style')\
#             .prefetch_related('product_item')\
#             .prefetch_related('product_item__discount')\
#             .prefetch_related('product_item__color')
#
#         return queryset


class ProductAPIDetailView(RetrieveAPIView):
    serializer_class = ProductSerializer
    lookup_field = 'slug'

    def get_queryset(self):
        queryset = Product.objects.all() \
            .select_related('brand') \
            .select_related('category') \
            .select_related('style') \
            .prefetch_related('product_item') \
            .prefetch_related('product_item__discount') \
            .prefetch_related('product_item__color')

        return queryset
