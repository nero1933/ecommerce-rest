from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from django_filters.rest_framework import DjangoFilterBackend

from ..filters.filters_products import ProductFilter
from ..models.models_products import Product
from ..serializers.serializers_products import ProductSerializer


class ProductAPIList(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = (DjangoFilterBackend, )
    filterset_class = ProductFilter

    # search_fields = ['brand', ]

    # def get_queryset(self):
    #     queryset = Product.objects.all().select_prefetch('productitem')
    #     return queryset

    # def get_serializer_context(self):
    #     context = super().get_serializer_context()
    #     # context["customer_id"] = self.kwargs['customer_id']
    #     # context["query_params"] = self.request.query_params
    #     print(self.get_discount_price())
    #     return context
    #
    # def get_discount_price(self):
    #     price = self.get_queryset()
    #     print(price)
