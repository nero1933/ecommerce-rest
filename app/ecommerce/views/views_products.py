from django.db.models import Prefetch
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from django_filters.rest_framework import DjangoFilterBackend

from ..filters.filters_products import ProductFilter
from ..models.models_products import Product, ProductItemSizeQuantity
from ..paginations.paginations_products import ProductPagination
from ..serializers.serializers_products import ProductSerializer, ProductDetailSerializer


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ProductSerializer
    pagination_class = ProductPagination
    filter_backends = (DjangoFilterBackend, )
    filterset_class = ProductFilter
    lookup_field = 'slug'

    def get_queryset(self):
        queryset = Product.objects\
            .select_related('brand', 'category', 'style') \
            .prefetch_related('reviews',
                              'product_item',
                              'product_item__discount',
                              'product_item__color',
                              'product_item__product_item_image',
                              Prefetch('product_item__product_item_size_quantity',
                                       queryset=ProductItemSizeQuantity.objects.filter(quantity__gt=0))
                              )

        return queryset

    def get_serializer_class(self):
        serializer_class = self.serializer_class
        if self.action == 'retrieve':
            serializer_class = ProductDetailSerializer

        return serializer_class

    # @action(methods=['post'], detail=True)
    # def reviews(self, request, slug=None):
    #     serializer_class = ReviewSerializer
    #     obj = self.get_object()
    #     print(request.data)
    #     serializer = ReviewSerializer(data=request.data)
    #     if serializer.is_valid():
    #         return Response({'status': 'review added'})
    #     # else:
    #     #     return Response(serializer.errors,
    #     #                     status=status.HTTP_400_BAD_REQUEST)
    #     return Response('hi')
