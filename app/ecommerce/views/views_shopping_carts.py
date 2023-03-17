from rest_framework import viewsets
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from ..models.models_shopping_cart import ShoppingCart, ShoppingCartItem
from ..serializers.serializers_shopping_cart import ShoppingCartItemSerializer, ShoppingCartSerializer, \
    ShoppingCartItemUpdateSerializer


class ShoppingCartItemViewSet(viewsets.ModelViewSet):
    serializer_class = ShoppingCartItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ShoppingCartItem.objects.filter(cart__user=self.request.user)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['user'] = self.request.user
        return context

    def get_serializer_class(self):
        serializer_class = self.serializer_class
        if self.action == 'update':
            serializer_class = ShoppingCartItemUpdateSerializer

        return serializer_class


class ShoppingCartAPIView(generics.ListAPIView):
    serializer_class = ShoppingCartSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = ShoppingCart.objects.filter(user=self.request.user) \
            .select_related('user') \
            .prefetch_related('shopping_cart_item')

        return queryset
