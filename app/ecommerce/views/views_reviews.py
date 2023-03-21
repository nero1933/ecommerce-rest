from django.contrib.auth.models import AnonymousUser
from rest_framework import viewsets, status
from rest_framework.generics import CreateAPIView
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



    # def get_object(self):
    #     pk = self.kwargs['pk']
    #     product_slug = self.kwargs['product_slug']
    #     user = self.request.user
    #     if self.action == 'update' and user.is_authenticated:
    #         return Review.objects.get(pk=pk, product__slug=product_slug, user=user)
    #     else:
    #         return None
    #
    #     return Review.objects.get(pk=pk, product__slug=product_slug)
    #
    # def update(self, request, *args, **kwargs):
    #     if not self.request.user.is_authenticated:
    #         return Response(status=status.HTTP_403_FORBIDDEN)
    #
    #     return super().update(self, request, *args, **kwargs)

class ReviewCreateAPIView(CreateAPIView):
    permission_classes = [IsReviewAllowed]
    serializer_class = ReviewCreateSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['order_id'] = self.kwargs['order_id']
        context['ordered_item_id'] = self.kwargs['ordered_item_id']
        return context

    # def get_object(self):
    #     #obj = OrderItem.objects.filter(pk=self.kwargs['ordered_item_id'])
    #     print(Order.objects.get(pk=self.kwargs['order_id']))
    #     #return Order.objects.get(pk=self.kwargs['order_id'])
    #     return Response('ok')
    #
    def get_object(self):
        return Order.objects.filter(pk=self.kwargs['order_id'], user=self.request.user, order_status=4)
