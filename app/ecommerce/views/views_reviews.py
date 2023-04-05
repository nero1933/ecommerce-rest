from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from ..models.models_reviews import Review
from ..paginations.paginations_reviews import ReviewPagination
from ..permissions.permissions_reviews import IsReviewAllowed
from ..serializers.serializers_revews import ReviewSerializer, ReviewCreateSerializer


class ReviewReadOnlyViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ReviewSerializer
    pagination_class = ReviewPagination

    def get_queryset(self):
        product_slug = self.kwargs['product_slug']
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
            context['user'] = self.request.user
        return context

    def get_queryset(self):
        return Review.objects.filter(user=self.request.user,
                                     order_item_id=self.kwargs['order_item_id'],
                                     )
