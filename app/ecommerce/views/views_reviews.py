from django.contrib.auth.models import AnonymousUser
from django.db import connection

from rest_framework import viewsets, status, generics
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ..models import OrderItem, Order
from ..models.models_reviews import Review
from ..permissions.permissions_reviews import IsCreatorOrReadOnly, IsReviewAllowed
from ..serializers.serializers_revews import ReviewSerializer, ReviewCreateSerializer


class ReviewReadOnlyViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        product_slug = self.kwargs['product_slug']
        print(self.request.method)
        return Review.objects.filter(product__slug=product_slug)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['product_slug'] = self.kwargs['product_slug']
        return context


class ReviewViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsReviewAllowed]
    serializer_class = ReviewCreateSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        if self.request.method == 'POST':
            context['order_id'] = self.kwargs['order_id']
            context['order_item_id'] = self.kwargs['order_item_id']
        print(f'LEN: {len(connection.queries)}')
        #[print(x) for x in connection.queries]
        return context

    def get_queryset(self):
        return Review.objects.filter(user=self.request.user,
                                     order_item_id=self.kwargs['order_item_id'],
                                     )
