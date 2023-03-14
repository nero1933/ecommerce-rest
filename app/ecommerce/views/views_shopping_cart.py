from django.http import HttpResponse
from rest_framework import viewsets
from rest_framework import generics

from rest_framework.permissions import IsAuthenticated
from rest_framework.utils import json
from rest_framework_simplejwt.authentication import JWTAuthentication

from ..models.models_shopping_cart import ShoppingCart, ShoppingCartItem
from ..serializers.serializers_shopping_cart import ShoppingCartItemSerializer, ShoppingCartSerializer


class ShoppingCartItemViewSet(viewsets.ModelViewSet):
    serializer_class = ShoppingCartItemSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        return ShoppingCartItem.objects.filter(cart__user=self.request.user)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['user'] = self.request.user
        return context


class ShoppingCartAPIView(generics.ListAPIView):
    serializer_class = ShoppingCartSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = ShoppingCart.objects.filter(user=self.request.user) \
            .select_related('user') \
            .prefetch_related('shopping_cart_item')

        return queryset
