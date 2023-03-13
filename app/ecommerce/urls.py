from django.urls import path, include

from rest_framework import routers

from .views.views_products import ProductViewSet
from .views.views_shopping_cart import ShoppingCartItemViewSet, ShoppingCartAPIView

router = routers.SimpleRouter()
router.register('products', ProductViewSet, basename='products')
router.register('shopping_cart_items', ShoppingCartItemViewSet, basename='shopping_cart_items')

urlpatterns = [
    path('api/v1/', include(router.urls)),
    path('api/v1/shopping_cart/', ShoppingCartAPIView.as_view(), name='shopping_cart'),
]
