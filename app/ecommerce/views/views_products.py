from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from django_filters.rest_framework import DjangoFilterBackend

from ..filters.filters_products import ProductFilter
from ..models.models_products import Product
from ..paginations.paginatioins_products import ProductPagination
from ..serializers.serializers_products import ProductListSerializer, ProductRetrieveSerializer


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ProductListSerializer
    pagination_class = ProductPagination
    filter_backends = (DjangoFilterBackend, )
    filterset_class = ProductFilter
    lookup_field = 'slug'

    def get_queryset(self):
        queryset = Product.objects.all()\
            .select_related('brand', 'category', 'style') \
            .prefetch_related('reviews') \
            .prefetch_related('product_item') \
            .prefetch_related('product_item__discount') \
            .prefetch_related('product_item__color') \
            .prefetch_related('product_item__product_item_size_quantity') \
            .prefetch_related('product_item__product_item_image')

        return queryset

    def get_serializer_class(self):
        serializer_class = self.serializer_class
        if self.action == 'retrieve':
            serializer_class = ProductRetrieveSerializer

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
