from django.urls import path, include

from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from .views.views_addresses import *

router = routers.SimpleRouter()
router.register(r'addresses', AddressViewSet, basename='addresses')
router.register(r'countries', CountryViewSet, basename='countries')

urlpatterns = [
    path('api/v1/auth/', include('rest_framework.urls')),
    path('api/v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/v1/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    path('api/v1/', include(router.urls)),
]

