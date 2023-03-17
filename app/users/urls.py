from django.urls import path, include

from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from .views.views_addresses import *
from .views.views_users import *

router = routers.SimpleRouter()
router.register(r'addresses', AddressViewSet, basename='addresses')
# router.register(r'payment_method', PaymentMethodViewSet, basename='payment_method')

urlpatterns = [
    path('api/v1/accounts/register', RegistrationAPIView.as_view(), name='register'),
    path('api/v1/accounts/login', LoginAPIView.as_view(), name='login'),
    path('api/v1/accounts/logout', LogoutAPIView.as_view(), name='logout'),
    path('api/v1/accounts/change-password', ChangePasswordAPIView.as_view(), name='change_password'),
    #path('api/v1/auth/', include('rest_framework.urls')),
    path('api/v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/v1/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    path('api/v1/', include(router.urls)),
]

