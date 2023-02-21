from rest_framework.generics import ListAPIView, RetrieveAPIView

from django_filters.rest_framework import DjangoFilterBackend

from ..filters.filters_products import ProductFilter
from ..utils.products.products_mixins import ProductAPIMixin


class ProductAPIList(ProductAPIMixin, ListAPIView):
    filter_backends = (DjangoFilterBackend, )
    filterset_class = ProductFilter


class ProductAPIDetailView(ProductAPIMixin, RetrieveAPIView):
    lookup_field = 'slug'
