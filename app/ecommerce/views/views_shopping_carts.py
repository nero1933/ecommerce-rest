import uuid

from rest_framework import viewsets
from rest_framework import generics

from ..serializers.serializers_shopping_cart import ShoppingCartItemSerializer, ShoppingCartSerializer, \
    ShoppingCartItemUpdateSerializer
from ..utils.shopping_cart.shopping_cart import ShoppingCartItemViewUtil


class ShoppingCartItemViewSet(ShoppingCartItemViewUtil, viewsets.ModelViewSet):
    serializer_class = ShoppingCartItemSerializer

    def get_queryset(self):
        return super().get_queryset()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        if self.request.user.is_authenticated:
            context['user'] = self.request.user
        else:
            context['session_id'] = self.request.session['unauth']

        return context

    def get_serializer_class(self):
        serializer_class = self.serializer_class
        if self.action == 'update':
            serializer_class = ShoppingCartItemUpdateSerializer

        return serializer_class


class ShoppingCartAPIView(ShoppingCartItemViewUtil, generics.ListAPIView):
    serializer_class = ShoppingCartSerializer

    def get_queryset(self):
        return super().get_queryset()
