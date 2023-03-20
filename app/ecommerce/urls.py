from django.urls import path, include

from rest_framework import routers

from .views.view_orders import OrderCreateAPIView, OrderDetailAPIView
from .views.views_products import ProductViewSet
from .views.views_shopping_carts import ShoppingCartItemViewSet, ShoppingCartAPIView

router = routers.SimpleRouter()
router.register('products', ProductViewSet, basename='products')
router.register('shopping_cart_items', ShoppingCartItemViewSet, basename='shopping_cart_items')

urlpatterns = [
    path('api/v1/', include(router.urls)),
    path('api/v1/shopping_cart/<int:pk>', ShoppingCartAPIView.as_view(), name='shopping_cart'),
    path('api/v1/create_order/', OrderCreateAPIView.as_view(), name='create_order'),
    path('api/v1/order/<int:pk>', OrderDetailAPIView.as_view(), name='order'),

]
