from django.urls import path, include

from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from .views import *

router = routers.SimpleRouter()
router.register(r'products', ProductViewSet, basename='products')

router_accounts = routers.SimpleRouter()
router_accounts.register(r'shopping_cart_items', ShoppingCartItemViewSet, basename='shopping_cart_items')
router_accounts.register(r'addresses', AddressViewSet, basename='addresses')
router_accounts.register(r'orders', OrderReadOnlyViewSet, basename='orders')

router_read_reviews = routers.SimpleRouter()
router_read_reviews.register(r'reviews', ReviewReadOnlyViewSet, basename='read_reviews')

# router.register(r'payment_method', PaymentMethodViewSet, basename='payment_method')

router_reviews = routers.SimpleRouter()
router_reviews.register(r'reviews', ReviewViewSet, basename='reviews')


urlpatterns = [
    path('api/v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/v1/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    path('api/v1/accounts/register', RegistrationAPIView.as_view(), name='register'),
    path('api/v1/accounts/register_confirm', register_confirm, name='register_confirm'),
    path('api/v1/accounts/login', LoginAPIView.as_view(), name='login'),
    path('api/v1/accounts/logout', LogoutAPIView.as_view(), name='logout'),
    path('api/v1/accounts/change_password', ChangePasswordAPIView.as_view(), name='change_password'),

    path('api/v1/accounts/<int:user_id>/shopping_cart', ShoppingCartAPIView.as_view(), name='shopping_cart'),
    path('api/v1/accounts/create_order', OrderCreateAPIView.as_view(), name='create_order'),
    path('api/v1/accounts/orders/<int:order_id>/product/<int:order_item_id>/', include(router_reviews.urls)),
    path('api/v1/accounts/', include(router_accounts.urls)),

    path('api/v1/', include(router.urls)),
    path('api/v1/products/<slug:product_slug>/', include(router_read_reviews.urls)),

    path('api/v1/accounts/test/<slug:token>', test, name='test'),
]
